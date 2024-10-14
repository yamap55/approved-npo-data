from unittest import mock

import pytest
from bs4 import BeautifulSoup
from requests import RequestException
from tenacity import RetryError

from approved_npo_data.util.scraping import scrape


class TestScraping:
    @pytest.fixture
    def mock_response(self):
        """モックされたレスポンス"""
        response = mock.Mock()
        response.status_code = 200
        response.content = b"<html><body><p>Hello World</p></body></html>"
        return response

    @pytest.fixture
    def mock_get(self, mock_response):
        """requests.getをモック化"""
        with mock.patch(
            "approved_npo_data.util.scraping.requests.get", return_value=mock_response
        ) as mocked_get:
            yield mocked_get

    @pytest.fixture
    def mock_get_failure(self):
        """requests.getが失敗するケースをモック化"""
        with mock.patch(
            "approved_npo_data.util.scraping.requests.get",
            side_effect=RequestException("Mocked Request Exception"),
        ) as mocked_get:
            yield mocked_get

    @pytest.fixture(autouse=True)
    def mock_sleep(self):
        """リトライの待機時間を無効化するために、time.sleepをモック化"""
        with mock.patch("tenacity.nap.time.sleep", return_value=None):
            yield

    def test_scrape_success(self, mock_get):
        """スクレイピング成功時のテスト"""
        url = "http://example.com"
        result = scrape(url)
        assert isinstance(result, BeautifulSoup)
        assert result.find("p").text == "Hello World"  # type: ignore

    def test_scrape_request_exception(self, mock_get_failure):
        """リクエスト例外のテスト"""
        url = "http://example.com"
        with pytest.raises(RetryError) as exc_info:
            scrape(url)
        assert isinstance(exc_info.value.last_attempt.exception(), ValueError)
        assert "URLの取得に失敗しました" in str(exc_info.value.last_attempt.exception())

    def test_scrape_retry_count(self, mock_get_failure):
        """リトライ回数のテスト"""
        url = "http://example.com"
        with pytest.raises(RetryError):
            scrape(url)
        # リトライ回数を確認
        assert mock_get_failure.call_count == 3
