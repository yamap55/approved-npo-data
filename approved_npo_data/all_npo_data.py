"""全NPO法人情報を取得する"""

import csv
from pathlib import Path

from approved_npo_data.util.file_downloader import download_file
from approved_npo_data.util.file_operations import extract_zip_file
from approved_npo_data.util.text_format import standardize_text_for_key

# 全NPO法人情報
# refs. https://www.npo-homepage.go.jp/npoportal/download/all
ALL_NPO_DATA_URL = "https://www.npo-homepage.go.jp/npoportal/download/zip/gyousei_000.zip"


def get_all_npo_data_file() -> Path:
    """全NPO法人情報のCSVファイルをダウンロードし、解凍したファイルのパスを返す"""
    download_path = download_file(ALL_NPO_DATA_URL)
    dir_path = extract_zip_file(download_path)

    csv_files = list(dir_path.glob("*.csv"))

    if len(csv_files) == 0 or len(csv_files) > 1:
        # ダウンロードしたファイルが正しいかは判別できないため、とりあえず1つのCSVファイルがあるという条件にしている  # noqa: E501
        raise Exception(f"Expected 1 CSV file, but found {len(csv_files)} files")
    return csv_files[0]


def read_csv(csv_path: Path) -> tuple[dict[str, dict[str, str]], list[str]]:
    """csvファイルを読み込みヘッダの1つ目をキーとした辞書を返す"""
    data_dict: dict[str, dict[str, str]] = {}

    with open(csv_path, encoding="cp932", newline="") as file:
        reader = csv.reader(file)

        header = next(reader)

        for row in reader:
            if not row:
                # 空行はスキップ
                continue
            key = standardize_text_for_key(row[0])
            data_dict[key] = {header[i]: row[i] for i, _ in enumerate(header)}
    return data_dict, header


def get_all_npo_data_from_url() -> tuple[dict[str, dict[str, str]], list[str]]:
    """全NPO法人情報をURLから取得する"""
    target_csv = get_all_npo_data_file()
    return read_csv(target_csv)
