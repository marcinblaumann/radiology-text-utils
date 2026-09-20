# Radiology Text Utils

Small Python utilities for cleaning and normalizing radiology report text.

This project explores simple, deterministic text-processing tools that can support radiology reporting workflows without modifying the medical meaning of the report.

## Features

- removal of duplicate whitespace
- normalization of punctuation spacing
- normalization of numerical ranges
- preservation of decimal notation
- basic paragraph cleanup
- no external dependencies

Example:

`5-6 mm` → `5 – 6 mm`

## Usage

```python
from radiology_text_utils import normalize_report_text

text = "Zmiana  o wymiarze 5-6 mm ."
print(normalize_report_text(text))
```

Output:

```text
Zmiana o wymiarze 5 – 6 mm.
```

The utility can also be used from the command line:

```bash
python -m radiology_text_utils "Zmiana  o wymiarze 5-6 mm ."
```

## Design principle

The utility performs deterministic formatting and whitespace normalization only.

It does not interpret medical findings, change medical terminology, or generate diagnostic conclusions.

## Testing

The repository includes automated tests covering whitespace, punctuation, numerical ranges, decimal notation, and paragraph handling.

## About

Created by [Marcin Blaumann](https://github.com/marcinblaumann), Consultant Radiologist with an interest in medical imaging, AI, speech recognition, and clinical workflow automation.

[Website](https://medical-ai.pl) · [LinkedIn](https://www.linkedin.com/in/marcin-b-a16b6a431)
