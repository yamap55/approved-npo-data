from approved_npo_data.util.text_format import standardize_text_for_key


def test_standardize_text_for_key_basic():
    text = "ＡＢＣ 123"
    expected = "ABC123"
    assert standardize_text_for_key(text) == expected


def test_standardize_text_for_key_remove_spaces():
    text = "ＡＢＣ　123　\t"
    expected = "ABC123"
    assert standardize_text_for_key(text) == expected


def test_standardize_text_for_key_mixed_characters():
    text = "Ａ ＢＣ １2３\tテスト"
    expected = "ABC123テスト"
    assert standardize_text_for_key(text) == expected


def test_standardize_text_for_key_no_change():
    text = "ABC123"
    expected = "ABC123"
    assert standardize_text_for_key(text) == expected


def test_standardize_text_for_key_empty_string():
    text = ""
    expected = ""
    assert standardize_text_for_key(text) == expected


def test_standardize_text_for_key_special_characters():
    text = "ＡＢＣ 123!@#"
    expected = "ABC123!@#"
    assert standardize_text_for_key(text) == expected
