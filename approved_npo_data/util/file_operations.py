"""ファイル操作に関するユーティリティ関数群"""

import csv
import tempfile
import zipfile
from collections.abc import Sequence
from datetime import datetime
from logging import getLogger
from pathlib import Path

from approved_npo_data.util.model_base import ModelBase

logger = getLogger(__name__)


def extract_zip_file(zip_path: Path, extract_to: Path | None = None) -> Path:
    """Zipファイルを解凍する"""
    if extract_to is None:
        extract_to = Path(tempfile.TemporaryDirectory().name)

    extract_to.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(extract_to)
    logger.debug(f"Files extracted to: {extract_to}")
    return extract_to


def save_csv(data: Sequence[ModelBase], output_path: Path) -> None:
    """CSVファイルでデータを保存する"""
    if not data:
        # NOTE: データが空の場合空のListが渡ってくるため、データの型が取れずヘッダが作成できない
        raise ValueError("空のデータでCSVを保存することはできません")

    with open(output_path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file, quoting=csv.QUOTE_ALL)
        writer.writerow(type(data[0]).get_csv_header())
        writer.writerows(row.to_csv_row() for row in data)
    logger.debug(f"Data saved to: {output_path}")


def get_output_path(base_path: Path, prefix: str = "output") -> Path:
    """出力ファイルのパスを取得する"""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    output_base_path = base_path / "output"
    output_base_path.mkdir(parents=True, exist_ok=True)

    return output_base_path / f"{prefix}_{timestamp}.csv"
