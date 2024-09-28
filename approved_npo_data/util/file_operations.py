"""ファイル操作に関するユーティリティ関数群"""

import tempfile
import zipfile
from logging import getLogger
from pathlib import Path

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
