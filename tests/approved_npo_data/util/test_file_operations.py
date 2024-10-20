import csv
import tempfile
import zipfile
from collections.abc import Sequence
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from unittest import mock

import pytest

from approved_npo_data.csv.csv_row import CsvRow
from approved_npo_data.util.file_operations import extract_zip_file, get_output_path, save_csv


class TestExtractZipFile:
    @pytest.fixture
    @staticmethod
    def temp_zip_file():
        """一時的なzipファイルを作成し、テスト後に削除する"""
        with tempfile.NamedTemporaryFile(suffix=".zip", delete=False) as temp_file:
            temp_zip_path = Path(temp_file.name)

        with zipfile.ZipFile(temp_zip_path, "w") as zipf:
            zipf.writestr("test.txt", "this is a test file")

        yield temp_zip_path

        temp_zip_path.unlink()

    def test_extract_zip_file_with_temp_directory(self, temp_zip_file):
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

    def test_extract_zip_file_to_specific_directory(self, temp_zip_file):
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
    def test_extract_zip_file_mocked_extract(self, mock_extractall, temp_zip_file):
        """Zipファイルのextractallが呼び出されることを確認"""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_dir_path = Path(temp_dir)
            extract_zip_file(temp_zip_file, temp_dir_path)

            mock_extractall.assert_called_once()


@dataclass(frozen=True)
class SampleCsvRow(CsvRow):
    Name: str
    Age: str
    City: str


class TestSaveCsv:
    @pytest.fixture
    @staticmethod
    def sample_data() -> list[SampleCsvRow]:
        return [
            SampleCsvRow(Name="Alice", Age="30", City="New York"),
            SampleCsvRow(Name="Bob", Age="25", City="San Francisco"),
        ]

    @pytest.fixture
    def output_path(self, tmp_path: Path, sample_data: Sequence[SampleCsvRow]) -> Path:
        output_path = tmp_path / "test.csv"
        save_csv(data=sample_data, output_path=output_path)
        return output_path

    def test_csv_file_creation(self, output_path: Path):
        assert output_path.exists(), "CSVファイルが作成されていません"

    def test_csv_header(self, output_path: Path):
        with open(output_path, newline="", encoding="utf-8") as file:
            reader = csv.reader(file, quoting=csv.QUOTE_ALL)
            header = next(reader)
        expected_header = SampleCsvRow.getHeader()
        assert header == expected_header, "ヘッダーが正しく保存されていません"

    def test_csv_data(self, output_path: Path, sample_data: Sequence[SampleCsvRow]):
        with open(output_path, newline="", encoding="utf-8") as file:
            reader = csv.reader(file, quoting=csv.QUOTE_ALL)
            next(reader)  # ヘッダーをスキップ
            rows = list(reader)
        expected_data = [row.getValues() for row in sample_data]
        assert rows == expected_data, "データが正しく保存されていません"

    def test_empty_data(self, tmp_path: Path):
        output_path = tmp_path / "test.csv"
        with pytest.raises(ValueError, match="空のデータでCSVを保存することはできません"):
            save_csv(data=[], output_path=output_path)


class TestGetOutputPath:
    @pytest.fixture
    @staticmethod
    def mock_datetime():
        """Datetimeモジュールをモックして、固定された日時を返す"""
        with mock.patch("approved_npo_data.util.file_operations.datetime") as mock_datetime:
            mock_datetime.now.return_value = datetime(2024, 9, 29, 12, 0, 0)
            mock_datetime.strftime.return_value = "20240929120000"
            yield mock_datetime

    def test_output_directory_creation(self, mock_datetime, tmp_path):
        """
        出力ディレクトリが正しく作成されること
        """
        base_path = tmp_path / "test_dir"
        result = get_output_path(base_path)

        output_dir = base_path / "output"
        assert output_dir.exists(), "出力ディレクトリが作成されていない"
        assert output_dir.is_dir(), "作成された出力ディレクトリがディレクトリではない"

        # 生成されたファイルパスが正しいか確認
        expected_path = output_dir / "output_20240929120000.csv"
        assert result == expected_path, "生成されたファイルパスが期待されるものと異なる"

    def test_output_file_with_custom_prefix(self, mock_datetime, tmp_path):
        """
        カスタムプレフィックスを指定した場合、正しいファイルパスが生成されること
        """
        base_path = tmp_path / "test_dir"
        prefix = "custom_prefix"

        result = get_output_path(base_path, prefix=prefix)

        expected_path = base_path / "output" / "custom_prefix_20240929120000.csv"
        assert (
            result == expected_path
        ), "カスタムプレフィックスを使用したファイルパスが期待されるものと異なる"
