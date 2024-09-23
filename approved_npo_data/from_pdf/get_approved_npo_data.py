"""
PDFファイルからNPO法人のデータを抽出し、CSVファイルに保存する

とりあえずノートブックから移植しただけなので以下で実行してください
>>> from approved_npo_data.from_pdf.get_approved_npo_data import main
>>> main()
"""

import csv
from datetime import datetime
from pathlib import Path

import pdfplumber

BASE_PATH = Path(".")
BASE_PATH.mkdir(parents=True, exist_ok=True)

CSV_HEADER = [
    "所轄庁コード",
    "所轄庁",
    "法人番号",
    "認定",
    "特例認定",
    "更新申請中",
    "法人名",
    "主たる事務所の所在地",
    "代表者氏名",
    "PST基準 相対値",
    "PST基準 絶対値",
    "PST基準 条例指定",
    "PST基準 条例指定 自治体名",
    "認定有効期間 自",
    "認定有効期間 至",
    "特例認定有効期間 自",
    "特例認定有効期間 至",
]


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
def extract_tables_from_pdf(pdf_path) -> list:
    """PDFファイルからテーブルを抽出する"""
    tables = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            for table in page.extract_tables():
                # テーブルの行ごとにクリーンアップし、ヘッダー行はスキップ
                tables.extend(clean_row(row) for row in table if not is_header_row(row))
    return tables


def get_pdf_path() -> Path:
    """PDFファイルのパスを取得する"""
    # NOTE: URLからダウンロードするとより良いと思うので関数に切り出している
    return BASE_PATH / "approved_npo_data/from_pdf" / "ninteimeibo.pdf"


def get_output_path() -> Path:
    """出力ファイルのパスを取得する"""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    output_base_path = BASE_PATH / "output"
    output_base_path.mkdir(parents=True, exist_ok=True)

    return output_base_path / f"output_{timestamp}.csv"


def save_csv(tables, csv_file_path) -> None:
    """CSVファイルでデータを保存する"""
    with open(csv_file_path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file, quoting=csv.QUOTE_ALL)
        writer.writerow(CSV_HEADER)
        writer.writerows(tables)


def main():
    """main"""
    pdf_path = get_pdf_path()
    tables = extract_tables_from_pdf(pdf_path)
    csv_file_path = get_output_path()
    save_csv(tables, csv_file_path)

    print(f"データが {csv_file_path} に保存されました。")
