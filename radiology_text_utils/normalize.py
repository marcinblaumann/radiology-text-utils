import re

# Unicode spaces that often come from Word or RIS systems (non-breaking,
# figure, narrow no-break, thin) plus tabs are treated as ordinary spaces.
_SPACE_LIKE = re.compile(r"[\t    ]")

# Fragments that must never be reformatted. They are swapped for
# placeholders before normalization and restored afterwards.
_PROTECTED = re.compile(
    r"[A-Za-z][A-Za-z0-9+.\-]*://[^\s]*[^\s.,;:!?)]"  # URLs
    r"|\b\d{1,2}:\d{2}(?::\d{2})?\b"  # times: 12:30, 08:15:00
    r"|\b\d+:\d+\b"  # ratios: 1:2
)

# A run of numbers joined by dashes. Two numbers form a range; three or more
# (dates such as 2024-03-15 or 15-03-2024, identifiers) are left untouched.
# Numbers glued to a letter (C5-6, L4-L5) are not matched, so spinal levels
# keep their original notation.
_NUMBER = r"-?\d+(?:[.,]\d+)?"
_DASH = r"\s*[-–—]\s*"
_NUMBER_CHAIN = re.compile(rf"(?<![\w.,]){_NUMBER}(?:{_DASH}{_NUMBER})+")
_RANGE = re.compile(rf"({_NUMBER}){_DASH}({_NUMBER})")

_PLACEHOLDER_START = ""
_PLACEHOLDER_END = ""


def _protect(text: str) -> tuple[str, list[str]]:
    saved: list[str] = []

    def store(match: re.Match) -> str:
        saved.append(match.group(0))
        # Encode the index with private-use characters (no digits),
        # so the number rules below never touch a placeholder.
        index = chr(0xE100 + len(saved) - 1)
        return f"{_PLACEHOLDER_START}{index}{_PLACEHOLDER_END}"

    return _PROTECTED.sub(store, text), saved


def _restore(text: str, saved: list[str]) -> str:
    return re.sub(
        rf"{_PLACEHOLDER_START}(.){_PLACEHOLDER_END}",
        lambda m: saved[ord(m.group(1)) - 0xE100],
        text,
    )


def _format_range(match: re.Match) -> str:
    chain = match.group(0)
    pair = _RANGE.fullmatch(chain)
    if pair is None:
        # Three or more numbers: a date or an identifier, not a range.
        return chain
    return f"{pair.group(1)} – {pair.group(2)}"


def normalize_report_text(text: str) -> str:
    """
    Normalize basic typography and whitespace in radiology report text.

    The function does not change medical terminology or attempt to
    interpret clinical content.
    """
    if not isinstance(text, str):
        raise TypeError("text must be a string")

    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = _SPACE_LIKE.sub(" ", text)
    text, saved = _protect(text)

    lines = []

    for line in text.split("\n"):
        line = re.sub(r" {2,}", " ", line).strip()

        # Remove spaces before punctuation and closing brackets,
        # and after opening brackets: "( 10 mm )" -> "(10 mm)".
        line = re.sub(r"\s+([,.;:!?)\]])", r"\1", line)
        line = re.sub(r"([(\[])\s+", r"\1", line)

        # Add a space after selected punctuation when appropriate.
        # A decimal comma between digits, e.g. 5,6 mm, is preserved.
        line = re.sub(r",(?!\d)(?=\S)", ", ", line)
        line = re.sub(r"([;:])(?=\S)", r"\1 ", line)

        # Normalize numeric ranges: 5-6, 5 - 6, 5–6 -> 5 – 6,
        # including negative values: -20 - -10 -> -20 – -10.
        line = _NUMBER_CHAIN.sub(_format_range, line)

        lines.append(line)

    result = "\n".join(lines)

    # Keep paragraphs, but remove excessive empty lines.
    result = re.sub(r"\n{3,}", "\n\n", result)

    return _restore(result.strip(), saved)
