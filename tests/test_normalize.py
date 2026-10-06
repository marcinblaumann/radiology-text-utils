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


def test_preserves_iso_date():
    assert normalize_report_text(
        "Badanie z dnia 2024-03-15."
    ) == "Badanie z dnia 2024-03-15."


def test_preserves_european_date():
    assert normalize_report_text(
        "Poprzednie badanie 15-03-2024."
    ) == "Poprzednie badanie 15-03-2024."


def test_preserves_time_and_ratio():
    assert normalize_report_text(
        "Godz. 12:30, stosunek 1:2."
    ) == "Godz. 12:30, stosunek 1:2."


def test_preserves_url():
    assert normalize_report_text(
        "Wytyczne: https://example.org/guide ."
    ) == "Wytyczne: https://example.org/guide."


def test_still_adds_space_after_colon_in_text():
    assert normalize_report_text(
        "Wnioski:bez zmian."
    ) == "Wnioski: bez zmian."


def test_keeps_spinal_levels_unchanged():
    assert normalize_report_text(
        "Poziom L4-L5 oraz C5-6."
    ) == "Poziom L4-L5 oraz C5-6."


def test_normalizes_negative_range():
    assert normalize_report_text(
        "Gęstość -20 - -10 HU."
    ) == "Gęstość -20 – -10 HU."


def test_normalizes_decimal_range():
    assert normalize_report_text(
        "Wymiar 5,5-6,5 mm."
    ) == "Wymiar 5,5 – 6,5 mm."


def test_does_not_touch_words_with_hyphen():
    assert normalize_report_text(
        "BI-RADS 4, obraz T1-zależny."
    ) == "BI-RADS 4, obraz T1-zależny."


def test_removes_spaces_inside_brackets():
    assert normalize_report_text(
        "Wymiar 12 mm ( poprzednio 10 mm )."
    ) == "Wymiar 12 mm (poprzednio 10 mm)."


def test_normalizes_non_breaking_spaces():
    assert normalize_report_text(
        "Zmiana  hipodensyjna."
    ) == "Zmiana hipodensyjna."
