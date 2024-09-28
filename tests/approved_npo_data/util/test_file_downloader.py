from pathlib import Path
from unittest.mock import MagicMock, mock_open, patch

import pytest
from requests.exceptions import HTTPError, RequestException

from approved_npo_data.util.file_downloader import download_file


@pytest.fixture
def mock_requests_get():
    with patch("approved_npo_data.util.file_downloader.requests.get") as mock_get:
        yield mock_get


@pytest.fixture
def mock_tempfile_mkdtemp():
    with patch("approved_npo_data.util.file_downloader.tempfile.mkdtemp") as mock_mkdtemp:
        yield mock_mkdtemp


@pytest.fixture
def mock_open_file():
    with patch(
        "approved_npo_data.util.file_downloader.open", mock_open(), create=True
    ) as mock_file:
        yield mock_file


def test_download_file_success(mock_requests_get, mock_tempfile_mkdtemp, mock_open_file):
    # モック設定: 正常なレスポンス
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.content = b"file content"
    mock_requests_get.return_value = mock_response
    mock_tempfile_mkdtemp.return_value = "/mock/temp/dir"

    url = "https://example.com/file.zip"
    expected_save_path = Path("/mock/temp/dir/file.zip")

    # 実行
    actual = download_file(url)

    # 検証
    mock_requests_get.assert_called_once_with(url)  # getが1回だけ呼ばれているか確認
    mock_open_file.assert_called_once_with(expected_save_path, "wb")
    mock_open_file().write.assert_called_once_with(b"file content")
    assert actual == expected_save_path


def test_download_file_with_specified_directory(mock_requests_get, mock_open_file):
    # モック設定: 正常なレスポンス
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.content = b"file content"
    mock_requests_get.return_value = mock_response

    url = "https://example.com/file.zip"
    specified_directory = Path("/specified/directory")
    expected_save_path = specified_directory / "file.zip"

    # 実行
    actual = download_file(url, save_directory_path=specified_directory)

    # 検証
    mock_requests_get.assert_called_once_with(url)
    mock_open_file.assert_called_once_with(expected_save_path, "wb")
    mock_open_file().write.assert_called_once_with(b"file content")
    assert actual == expected_save_path


def test_download_file_network_error(mock_requests_get):
    # モック設定: ネットワークエラー発生
    mock_requests_get.side_effect = RequestException("Network error")

    url = "https://example.com/file.zip"

    with pytest.raises(Exception, match="Failed to download the file:.*"):
        download_file(url)

    mock_requests_get.assert_called_once_with(url)


def test_download_file_invalid_status_code(mock_requests_get):
    # モック設定: 404エラー
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = HTTPError("404 Client Error")
    mock_requests_get.return_value = mock_response

    url = "https://example.com/file.zip"

    with pytest.raises(Exception, match="Failed to download the file:"):
        download_file(url)

    mock_requests_get.assert_called_once_with(url)
