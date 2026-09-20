import re


def normalize_report_text(text: str) -> str:
    """
    Normalize basic typography and whitespace in radiology report text.

    The function does not change medical terminology or attempt to
    interpret clinical content.
    """
    if not isinstance(text, str):
        raise TypeError("text must be a string")

    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = text.replace("\t", " ")

    lines = []

    for line in text.split("\n"):
        line = re.sub(r" {2,}", " ", line).strip()

        # Remove spaces before punctuation.
        line = re.sub(r"\s+([,.;:!?])", r"\1", line)

        # Add a space after selected punctuation when appropriate.
        # A decimal comma between digits, e.g. 5,6 mm, is preserved.
        line = re.sub(r",(?!\d)(?=\S)", ", ", line)
        line = re.sub(r"([;:])(?=\S)", r"\1 ", line)

        # Normalize numeric ranges: 5-6, 5 - 6, 5–6 -> 5 – 6
        line = re.sub(r"(?<=\d)\s*[-–—]\s*(?=\d)", " – ", line)

        lines.append(line)

    result = "\n".join(lines)

    # Keep paragraphs, but remove excessive empty lines.
    result = re.sub(r"\n{3,}", "\n\n", result)

    return result.strip()
