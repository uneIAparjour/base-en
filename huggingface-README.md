---
license: cc-by-4.0
language:
  - en
pretty_name: "Base uneIAparjour.fr — English — Generative AI Apps"
size_categories:
  - 1K<n<10K
task_categories:
  - text-classification
tags:
  - ai-tools
  - generative-ai
  - curation
  - english
  - daily-updates
source_datasets:
  - uneIAparjour/base
dataset_info:
  features:
    - name: Title
      dtype: string
    - name: Description
      dtype: string
    - name: URL on uneiaparjour.fr
      dtype: string
    - name: Category 1
      dtype: string
    - name: Category 2
      dtype: string
    - name: Category 3
      dtype: string
    - name: Category 4
      dtype: string
    - name: Category 5
      dtype: string
    - name: Category 6
      dtype: string
    - name: Publication Date
      dtype: string
---

# Base uneIAparjour.fr — English — Generative AI Apps

Open dataset listing **one generative AI tool per day** since February 16, 2023, featured on [uneiaparjour.fr](https://www.uneiaparjour.fr/en/) and translated to English.

## Description

Every day, a new free or freemium generative AI tool is tested, described and categorized — originally in French, then translated to English by a dedicated pipeline once available. This dataset is the English mirror of [`uneIAparjour/base`](https://huggingface.co/datasets/uneIAparjour/base), the original French dataset.

## Content

- **1294 tools** (as of 06/09/2026)
- **33 categories**: chatbot, images, text, video, music, education, open source…
- **Period** : February 16, 2023 → 06/09/2026
- **Language**: English (translated)
- **Coverage**: not 100% of the French base yet — only tools with a published English translation appear here

## Fields

| Field | Description |
|---|---|
| `Title` | Tool name |
| `Description` | Editorial summary of the tool |
| `URL on uneiaparjour.fr` | Link to the full English article |
| `Category 1` to `Category 6` | Up to 6 categories |
| `Publication Date` | Date, format DD-MM-YYYY |

## Usage

```python
from datasets import load_dataset

dataset = load_dataset("uneIAparjour/base-en")
df = dataset["train"].to_pandas()

# Image generation tools
images = df[df["Category 1"] == "Images"]
print(f"{len(images)} image generation tools")
```

## Source and updates

Source: [GitHub](https://github.com/uneIAparjour/base-en)
Site: [uneiaparjour.fr/en](https://www.uneiaparjour.fr/en/)
French dataset: [uneIAparjour/base](https://huggingface.co/datasets/uneIAparjour/base)

## Author and license

**Bertrand Formet**

License: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)

> uneIAparjour.fr English dataset as of 06/09/2026, Bertrand Formet, CC BY 4.0 license.
