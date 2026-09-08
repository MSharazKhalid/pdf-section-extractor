# PDF Section Extractor

Four small tools for pulling text out of a folder of PDFs.

- `whole_extract.py` - searches the whole page text for keywords
- `section_extract.py` - searches only inside a named section
- `section_extract_below.py` - searches the text below a named section
- `draw_bounding_box.py` - draws boxes on the page so you can see where
  text sits, useful when calibrating the other three

## Setup

```
pip install -r requirements.txt
```

## Run

```
python whole_extract.py
```

## What to edit before running

The `EDIT THIS` block at the top of each file - `pdf_folder`.

## Never commit

Patient or client data (`.xlsx`, `.pdf`, `.csv`), `service_account.json`,
and chromedriver binaries. All are covered by `.gitignore`.
