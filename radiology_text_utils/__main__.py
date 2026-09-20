import argparse
import sys

from .normalize import normalize_report_text


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Clean and normalize radiology report text."
    )
    parser.add_argument(
        "text",
        nargs="?",
        help="Text to normalize. If omitted, input is read from stdin.",
    )

    args = parser.parse_args()

    if args.text is None:
        text = sys.stdin.read()
    else:
        text = args.text

    print(normalize_report_text(text))


if __name__ == "__main__":
    main()
