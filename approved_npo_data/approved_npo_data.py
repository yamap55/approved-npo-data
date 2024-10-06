"""
認定NPO法人のデータを取得する

CSV出力する際の関数も含まれている
"""

from pathlib import Path
from tempfile import TemporaryDirectory

import pdfplumber

from approved_npo_data.csv.csv_row import ApprovedNpoRow
from approved_npo_data.scraping.npoportal_approved_npo_list.all_approved_npo_list_url import (
    get_approved_npo_data_url,
)
from approved_npo_data.util.file_downloader import download_file


def is_header_row(row):
    """
    与えられた行がヘッダ行であるかを判定する

    ※判定基準はPDFの構造に依存するため、正しく動作しない場合にはルールを確認すること
    """
    # 最初のカラムが「所轄庁コード」または最初と2番目のカラムが空の場合、ヘッダー行と見なす。
    return row[0] == "所轄庁コード" or (row[0] is None and row[1] is None)


def clean_row(row):
    """
    各セル内の改行を除去する。None値は空文字に変換。
    """
    return [cell.replace("\n", "").replace("\r", "") if cell else "" for cell in row]


# PDFからテーブルを抽出するための関数
def extract_tables_from_pdf(pdf_path) -> list[ApprovedNpoRow]:
    """PDFファイルからテーブルを抽出する"""
    tables = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            for table in page.extract_tables():
                # テーブルの行ごとにクリーンアップし、ヘッダー行はスキップ
                tables.extend(
                    ApprovedNpoRow(*clean_row(row)) for row in table if not is_header_row(row)
                )
    return tables


def download_approved_npo_data(temp_dir: Path) -> Path:
    """認定NPO法人のデータをダウンロードする"""
    url = get_approved_npo_data_url()
    return download_file(url, temp_dir)


def get_approved_npo_data() -> list[ApprovedNpoRow]:
    """認定NPO法人のデータを取得する"""
    with TemporaryDirectory() as temp_dir:
        pdf_path = download_approved_npo_data(Path(temp_dir))
        return extract_tables_from_pdf(pdf_path)
