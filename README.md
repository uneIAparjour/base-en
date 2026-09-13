# Base uneIAparjour.fr — English

Open dataset listing, in English, the generative AI tools featured daily on [uneiaparjour.fr](https://www.uneiaparjour.fr/en/) since February 16, 2023.

This is the English counterpart of [`uneIAparjour/base`](https://github.com/uneIAparjour/base) (the original French dataset). It is not a translation pipeline itself — it reads directly from the site's own English RSS feed, which already carries translated titles, descriptions and categories produced by the separate [`uneiaparjour-en-translation`](https://github.com/uneIAparjour/uneiaparjour-en-translation) project. Coverage here can lag slightly behind the French base while an article's English translation is still in progress.

## Content

One tool per day, described and categorized:

| Field | Description |
|---|---|
| `Title` | Tool name |
| `Description` | Editorial summary |
| `URL on uneiaparjour.fr` | Article on the site |
| `Category 1` to `Category 6` | Up to 6 categories out of 33 |
| `Publication Date` | Publication date (DD/MM/YYYY) |

## Available formats

- **`base-uneiaparjour-en.ods`** — Source format (LibreOffice/Excel)
- **`base-uneiaparjour-en.csv`** — CSV export (UTF-8, comma-separated)

The CSV file is regenerated automatically on every ODS update.

## Automatic updates

The base is updated automatically every night via GitHub Actions, 2 hours after the translation pipeline's own daily run:

- A script fetches newly-published English articles from the site's `/en/feed/` RSS
- The ODS, the CSV and this README are updated and committed automatically
- The Hugging Face dataset is synced right after

The workflow can also be triggered manually from the repo's Actions tab.

## Categories

Same 33 categories as the French base, translated: access, application, archives, automation, comics, chatbot, data, documents, education, FR / EU, children's stories, images, 3D images, infographic, video game, languages, LLM, mindmap, music, browser, open source, presentation, qr code, quiz & flashcards, research, no account needed, website, text, tutorial, unlimited use, video, voice, youtube

## Key figures

- **1302 tools** listed (as of 13/09/2026)
- **33 categories**
- Range: 16/02/2023 → 13/09/2026

## Used by

- **[uneIAparjour/recherche-outils](https://github.com/uneIAparjour/recherche-outils)** — the site's fullscreen search overlay reads this CSV directly (live, client-side) to power search and category filtering on the English pages. The French overlay reads the original `base` CSV the same way.

## Also available on

- 🤗 [Hugging Face Datasets](https://huggingface.co/datasets/uneIAparjour/base-en) — Interactive exploration and API

## License

**CC BY 4.0** — [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/)

To cite this dataset:

> uneIAparjour.fr English dataset, Bertrand Formet, [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

## Author
🔗 [Bertrand Formet](https://www.linkedin.com/in/bertrandformet/)

**Links**
- 🌐 [uneiaparjour.fr/en](https://www.uneiaparjour.fr/en/)
- 🇫🇷 [French dataset](https://github.com/uneIAparjour/base)
- 📰 [Newsletter (French only for now)](https://uneiaparjour.substack.com/)
