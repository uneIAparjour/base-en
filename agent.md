# agent.md — Base uneIAparjour.fr (English)

## Context

This repository contains the English dataset for uneiaparjour.fr: a generative AI tool featured daily since February 16, 2023 by Bertrand Formet, translated to English by a separate pipeline ([`uneiaparjour-en-translation`](https://github.com/uneIAparjour/uneiaparjour-en-translation)).

This dataset is **derived, not authoritative** — the French base ([`uneIAparjour/base`](https://github.com/uneIAparjour/base)) is the source of truth for which tools exist and their original data. This repository only mirrors whatever has already been translated and published in English at the time it last ran.

**1296 tools** referenced (as of 07/09/2026).

## File structure

```
base-uneiaparjour-en.ods    # Source of truth for this dataset (LibreOffice Calc)
base-uneiaparjour-en.csv    # Automatic export (do not edit by hand)
README.md                    # Public documentation
agent.md                     # This file (instructions for AI agents)
```

## Data schema

| Column | Type | Required | Description |
|---|---|---|---|
| Title | text | yes | Tool name |
| Description | text | yes | Full editorial summary |
| URL on uneiaparjour.fr | URL | yes | Link to the English article |
| Category 1 to 6 | text | cat. 1 yes | Among the 33 existing categories |
| Publication Date | date | yes | Format DD/MM/YYYY |

## Hard rules

1. **Never modify URLs by hand** — extract them faithfully, never invent them
2. **Never edit the CSV directly** — it is generated automatically from the ODS
3. **Date format**: always `DD/MM/YYYY`
4. **Categories**: use only the 33 existing categories, respect exact casing (lowercase except `FR / EU` and `LLM`)
5. **One article = one day** — except rare exceptions (mirrors the French base)
6. **Order**: reverse-chronological (most recent first)

## The 33 valid categories

```
access, application, archives, automation, comics, chatbot, data,
documents, education, FR / EU, children's stories, images, 3D images,
infographic, video game, languages, LLM, mindmap, music, browser,
open source, presentation, qr code, quiz & flashcards, research,
no account needed, website, text, tutorial, unlimited use, video,
voice, youtube
```

## Coverage gap vs. the French base

Not every French tool has an English counterpart yet — as of this writing, translation coverage is around 1277 of ~1289 tools in the official dataset. An entry only appears here once its English translation is published (`/en/...` URL live). Do not treat a missing entry here as a data error; cross-check against the French base and `uneiaparjour-en-translation`'s `state/translations.json` before assuming something is broken.

## Source of truth

- **Publication dates**: copied from the French original at translation time — not the English RSS feed's own timestamp, which reflects when the translation was published, not when the tool was originally featured (this repo relies on the translation pipeline having already set this correctly on the WordPress side)
- **Descriptions**: the English WordPress article's own content, as translated
- **Categories**: the English WordPress categories of each article, as translated

## Updates

The base is updated **automatically every night** via the `nightly-update.yml` workflow (GitHub Actions, 08:00 UTC — 2 hours after the translation pipeline's own daily translate+publish run, so newly-published English articles are already live): reads the site's `/en/feed/` RSS, inserts new articles into the ODS, generates the CSV, updates the READMEs, and syncs to Hugging Face.

Unlike the French base, this repository has no manual-ODS-edit path — it is meant to stay a pure mirror of what the translation pipeline has already published, not a place for original curation.
