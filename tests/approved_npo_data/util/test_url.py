from approved_npo_data.util.url import extract_embedded_url


class TestExtractEmbeddedUrl:
    def test_valid_url(self):
        original_url = "https://www.example.com/external/?url=https%3A%2F%2Fwww.example.org%2Fpath%2Fto%2Fresource"
        expected = "https://www.example.org/path/to/resource"
        actual = extract_embedded_url(original_url)
        assert actual == expected

    def test_valid_url_with_custom_param(self):
        original_url = "https://www.example.com/external/?link=https%3A%2F%2Fwww.example.org%2Fpath%2Fto%2Fresource"
        expected = "https://www.example.org/path/to/resource"
        actual = extract_embedded_url(original_url, param_name="link")
        assert actual == expected

    def test_no_embedded_url(self):
        original_url = "https://www.example.com/external/?other_param=some_value"
        expected = ""
        actual = extract_embedded_url(original_url)
        assert actual == expected

    def test_empty_url(self):
        original_url = ""
        expected = ""
        actual = extract_embedded_url(original_url)
        assert actual == expected
