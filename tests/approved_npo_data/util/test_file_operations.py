import tempfile
import zipfile
from pathlib import Path
from unittest import mock

import pytest

from approved_npo_data.util.file_operations import extract_zip_file


@pytest.fixture
def temp_zip_file():
    """一時的なzipファイルを作成し、テスト後に削除する"""
    with tempfile.NamedTemporaryFile(suffix=".zip", delete=False) as temp_file:
        temp_zip_path = Path(temp_file.name)

    with zipfile.ZipFile(temp_zip_path, "w") as zipf:
        zipf.writestr("test.txt", "this is a test file")

    yield temp_zip_path

    temp_zip_path.unlink()


def test_extract_zip_file_with_temp_directory(temp_zip_file):
    """extract_zip_file関数が正しく解凍を行うかテスト"""
    # extract_toがNoneの場合、一時ディレクトリに解凍されることを確認
    output_dir = extract_zip_file(temp_zip_file)

    # 解凍後のディレクトリ内にファイルが存在することを確認
    extracted_file = output_dir / "test.txt"
    assert extracted_file.exists()

    # 解凍されたファイルの内容を確認
    with extracted_file.open() as f:
        content = f.read()
    assert content == "this is a test file"


def test_extract_zip_file_to_specific_directory(temp_zip_file):
    """指定したディレクトリに解凍が行われるかテスト"""
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_dir_path = Path(temp_dir)
        output_dir = extract_zip_file(temp_zip_file, temp_dir_path)

        # 解凍先ディレクトリが正しく設定されていることを確認
        assert output_dir == temp_dir_path

        # 解凍されたファイルの存在を確認
        extracted_file = output_dir / "test.txt"
        assert extracted_file.exists()


@mock.patch("approved_npo_data.util.file_operations.zipfile.ZipFile.extractall")
def test_extract_zip_file_mocked_extract(mock_extractall, temp_zip_file):
    """Zipファイルのextractallが呼び出されることを確認"""
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_dir_path = Path(temp_dir)
        extract_zip_file(temp_zip_file, temp_dir_path)

        mock_extractall.assert_called_once()
