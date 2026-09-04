#!/usr/bin/env python3
import re
import sys
import time
from datetime import datetime, timezone
from html import unescape
from urllib.parse import urlparse, parse_qs, urlencode

import feedparser
from odf.opendocument import load
from odf.table import Table, TableRow, TableCell
from odf.text import P

ODS_PATH = "base-uneiaparjour-en.ods"
FEED_URL = "https://www.uneiaparjour.fr/en/feed/"
MAX_CATEGORIES = 6
DELAY = 1.0


def get_cell_text(cell):
    ps = cell.getElementsByType(P)
    if not ps:
        return ''
    p = ps[0]
    text = ''
    for node in p.childNodes:
        if hasattr(node, 'data'):
            text += node.data
        elif hasattr(node, 'childNodes'):
            for child in node.childNodes:
                if hasattr(child, 'data'):
                    text += child.data
    return text


def get_cell_at_index(row, target_index):
    cells = row.getElementsByType(TableCell)
    current = 0
    for cell in cells:
        repeat = int(cell.getAttribute('numbercolumnsrepeated') or 1)
        if current + repeat > target_index:
            return cell
        current += repeat
    return None


def strip_html(html_text):
    text = re.sub(r"<[^>]+>", "", html_text)
    text = unescape(text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def extract_first_paragraph(entry):
    content = ""
    if hasattr(entry, "content") and entry.content:
        content = entry.content[0].get("value", "")
    if not content:
        content = entry.get("description", "") or entry.get("summary", "")
    matches = re.findall(r"<p[^>]*>(.*?)</p>", content, re.DOTALL | re.IGNORECASE)
    for match in matches:
        text = strip_html(match)
        if text:
            return text
    return strip_html(content)


def parse_ods_date(date_str):
    try:
        dt = datetime.strptime(date_str, "%d/%m/%Y")
        return dt.replace(hour=23, minute=59, second=59, tzinfo=timezone.utc)
    except (ValueError, TypeError):
        return None


def parse_rss_date(date_str):
    try:
        return datetime.strptime(date_str, "%a, %d %b %Y %H:%M:%S %z")
    except (ValueError, TypeError):
        return None


def format_date(date_str):
    try:
        dt = datetime.strptime(date_str, "%a, %d %b %Y %H:%M:%S %z")
        return dt.strftime("%d/%m/%Y")
    except (ValueError, TypeError):
        return ""


def build_paged_url(base_url, page):
    parsed = urlparse(base_url)
    params = parse_qs(parsed.query)
    params["paged"] = [str(page)]
    new_query = urlencode(params, doseq=True)
    return parsed._replace(query=new_query).geturl()


def get_existing_urls(base_sheet):
    """Fetch every URL already present in the ODS (column 2)."""
    urls = set()
    rows = base_sheet.getElementsByType(TableRow)
    for row in rows[1:]:
        cell = get_cell_at_index(row, 2)
        if cell:
            url = get_cell_text(cell).strip()
            if url:
                urls.add(url)
    return urls


def get_last_date_from_ods(ods_path):
    doc = load(ods_path)
    sheets = doc.spreadsheet.getElementsByType(Table)
    base_sheet = next(s for s in sheets if s.getAttribute('name') == 'Base')
    rows = base_sheet.getElementsByType(TableRow)
    for row in rows[1:]:
        cell = get_cell_at_index(row, 9)
        if cell is None:
            continue
        date_str = get_cell_text(cell).strip()
        if date_str:
            print(f"Last date read: '{date_str}'")
            return parse_ods_date(date_str), doc
    # Empty base (first run, or not yet seeded) — not an error, just means
    # "fetch everything the EN feed has" (last_date=None short-circuits the
    # cutoff check in fetch_new_entries below, same as the FR script, just
    # never hit there since that base has been running for years).
    print("Empty base — first run, fetching the full EN feed history.")
    return None, doc


def fetch_new_entries(last_date):
    new_entries = []
    seen_links = set()
    page = 1

    while True:
        url = build_paged_url(FEED_URL, page) if page > 1 else FEED_URL
        print(f"RSS page {page}")
        feed = feedparser.parse(url)

        if not feed.entries:
            break

        found_older = False
        new_on_page = 0
        for entry in feed.entries:
            link = entry.get("link", "")
            if link in seen_links:
                continue
            seen_links.add(link)

            pub_date = parse_rss_date(entry.get("published", ""))
            if pub_date and last_date and pub_date <= last_date:
                found_older = True
                continue

            new_entries.append(entry)
            new_on_page += 1

        print(f"   {new_on_page} new (total: {len(new_entries)})")

        if found_older:
            break

        page += 1
        time.sleep(DELAY)

    return new_entries


def make_cell(val):
    """Creates an ODS cell with an explicit string valuetype, readable by pandas."""
    cell = TableCell(valuetype="string")
    p = P()
    p.addText(str(val))
    cell.addElement(p)
    return cell


def make_row(entry):
    categories = [tag.term for tag in getattr(entry, "tags", [])]

    # Same defensive exclusion as the FR base's Focus/newsletter filter —
    # shouldn't ever actually fire here (only tool-review posts get an EN
    # translation in the first place, per the translation pipeline's own
    # dataset scoping), but free to keep and matches the FR script's shape.
    if any(c.strip() == 'Focus' for c in categories):
        return None

    cats = (categories + [""] * MAX_CATEGORIES)[:MAX_CATEGORIES]

    values = [
        entry.get("title", ""),
        extract_first_paragraph(entry),
        entry.get("link", ""),
    ] + cats + [format_date(entry.get("published", ""))]

    row = TableRow()
    for val in values:
        row.addElement(make_cell(val))
    return row


def main():
    print("Incremental EN ODS update...")

    last_date, _ = get_last_date_from_ods(ODS_PATH)
    if last_date:
        print(f"Last article: {last_date.strftime('%d/%m/%Y')}")

    new_entries = fetch_new_entries(last_date)

    if not new_entries:
        print("Base up to date")
        sys.exit(0)

    doc2 = load(ODS_PATH)
    sheets = doc2.spreadsheet.getElementsByType(Table)
    base_sheet = next(s for s in sheets if s.getAttribute('name') == 'Base')
    rows = base_sheet.getElementsByType(TableRow)

    existing_urls = get_existing_urls(base_sheet)
    print(f"Existing URLs: {len(existing_urls)}")

    insert_before_row = None
    for row in rows[1:]:
        cell = get_cell_at_index(row, 0)
        if cell and get_cell_text(cell).strip():
            insert_before_row = row
            break
    if insert_before_row is None:
        insert_before_row = rows[1]

    inserted = 0
    skipped_focus = 0
    skipped_duplicate = 0
    rows_to_insert = []

    new_entries.sort(
        key=lambda e: parse_rss_date(e.get("published", "")) or datetime.min.replace(tzinfo=timezone.utc),
        reverse=True
    )

    for entry in new_entries:
        link = entry.get("link", "")
        if link in existing_urls:
            skipped_duplicate += 1
            print(f"   Duplicate skipped: {entry.get('title', '')}")
            continue

        row = make_row(entry)
        if row is not None:
            rows_to_insert.append(row)
            existing_urls.add(link)
        else:
            skipped_focus += 1

    for row in reversed(rows_to_insert):
        base_sheet.insertBefore(row, insert_before_row)
        inserted += 1

    if skipped_focus:
        print(f"{skipped_focus} Focus skipped")
    if skipped_duplicate:
        print(f"{skipped_duplicate} duplicate(s) skipped")

    if inserted > 0:
        doc2.save(ODS_PATH)
        print(f"{inserted} article(s) added")
    else:
        print("Nothing to add")

    sys.exit(0)


if __name__ == "__main__":
    main()
