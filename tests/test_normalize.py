from radiology_text_utils import normalize_report_text


def test_removes_extra_spaces():
    assert normalize_report_text(
        "Łąkotka  przyśrodkowa   bez szczelin."
    ) == "Łąkotka przyśrodkowa bez szczelin."


def test_removes_space_before_punctuation():
    assert normalize_report_text(
        "ACL zachowane , bez cech uszkodzenia ."
    ) == "ACL zachowane, bez cech uszkodzenia."


def test_normalizes_numeric_range():
    assert normalize_report_text(
        "Zmiana o wymiarze 5-6 mm."
    ) == "Zmiana o wymiarze 5 – 6 mm."


def test_preserves_decimal_comma():
    assert normalize_report_text(
        "Grubość 5,6 mm."
    ) == "Grubość 5,6 mm."


def test_normalizes_tabs():
    assert normalize_report_text(
        "MRI\tkolana"
    ) == "MRI kolana"


def test_limits_empty_lines():
    assert normalize_report_text(
        "Pierwszy akapit.\n\n\n\nDrugi akapit."
    ) == "Pierwszy akapit.\n\nDrugi akapit."
