"""全NPO法人情報を取得する"""

import csv
from pathlib import Path
from tempfile import TemporaryDirectory

from approved_npo_data.csv.csv_row import AllNpoDataRow
from approved_npo_data.util.file_downloader import download_file
from approved_npo_data.util.file_operations import extract_zip_file

# 全NPO法人情報
# refs. https://www.npo-homepage.go.jp/npoportal/download/all
ALL_NPO_DATA_URL = "https://www.npo-homepage.go.jp/npoportal/download/zip/gyousei_000.zip"


def get_all_npo_data_file(temp_dir: Path) -> Path:
    """全NPO法人情報のCSVファイルをダウンロードし、解凍したファイルのパスを返す"""
    download_path = download_file(ALL_NPO_DATA_URL, temp_dir)
    dir_path = extract_zip_file(download_path)

    csv_files = list(dir_path.glob("*.csv"))

    if len(csv_files) == 0 or len(csv_files) > 1:
        # ダウンロードしたファイルが正しいかは判別できないため、とりあえず1つのCSVファイルがあるという条件にしている  # noqa: E501
        raise Exception(f"Expected 1 CSV file, but found {len(csv_files)} files")
    return csv_files[0]


def read_csv(csv_path: Path) -> dict[str, AllNpoDataRow]:
    """csvファイルを読み込み、法人番号をキーとした辞書を返す"""
    data_dict: dict[str, AllNpoDataRow] = {}

    with open(csv_path, encoding="cp932", newline="") as file:
        reader = csv.reader(file)

        # ヘッダを捨てる
        next(reader)

        for row in reader:
            if not row:
                # 空行はスキップ
                continue
            all_npo = AllNpoDataRow(*row)
            # 法人番号をキーとして辞書に追加
            data_dict[all_npo.corporate_number] = all_npo
    return data_dict


def get_all_npo_data_from_url() -> dict[str, AllNpoDataRow]:
    """全NPO法人情報をURLから取得する"""
    with TemporaryDirectory() as temp_dir:
        target_csv = get_all_npo_data_file(Path(temp_dir))
        return read_csv(target_csv)
