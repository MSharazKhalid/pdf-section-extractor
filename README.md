# PDF Section Extractor

Four tools for pulling text out of a folder of PDFs - by whole page, by named
section, or by what sits below a section heading.

![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?logo=python&logoColor=white) ![pdfplumber](https://img.shields.io/badge/pdfplumber-FF6B6B) ![License](https://img.shields.io/badge/License-MIT-2ea44f)

## What it does

Searching a PDF for a keyword is easy. Searching *only inside a particular section*
is not - and that is usually what you actually need when the same term means
different things in different parts of a document.

| Script | Searches |
|---|---|
| `whole_extract.py` | The full text of every page |
| `section_extract.py` | Only inside a named section |
| `section_extract_below.py` | Only the text that falls below a named section heading |
| `draw_bounding_box.py` | Nothing - it draws boxes on the page so you can see where text actually sits |

`draw_bounding_box.py` is the one that makes the others usable. Section boundaries
depend on coordinates, and coordinates differ between document templates. Render
the boxes first, see where the text really is, then calibrate the other three.

## Requirements

- Python 3.9+
- `pandas`, `pdfplumber`, `Pillow`, `openpyxl`

## Install

```bash
pip install -r requirements.txt
```

## Configure

Each script has an `EDIT THIS` block at the top. Set `pdf_folder` to the directory
holding your PDFs.

## Run

```bash
python whole_extract.py
```

## Notes on data

This repository contains **no client or patient data**. `.gitignore` already excludes
`.xlsx`, `.pdf` and `.csv` files, `service_account.json`, and chromedriver binaries -
keep it that way if you fork this.

## License

MIT © Muhammad Sharaz Khalid - see [LICENSE](LICENSE).
