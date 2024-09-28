"""
ファイルをダウンロードするための関数群
"""

import tempfile
from logging import getLogger
from pathlib import Path

import requests
from requests.exceptions import RequestException

logger = getLogger(__name__)


def download_file(url: str, save_directory_path: Path | None = None) -> Path:
    """
    Download a file from a URL and save it to a directory.
    """
    if save_directory_path is None:
        save_directory_path = Path(tempfile.mkdtemp())

    # URLにクエリパラメータやリダイレクトされるような場合は考慮しない
    file_name = url.split("/")[-1]
    save_path = save_directory_path / file_name

    try:
        response = requests.get(url)
        response.raise_for_status()
    except RequestException as e:
        raise Exception(f"Failed to download the file: {e}") from e

    with open(save_path, "wb") as file:
        file.write(response.content)
    logger.info(f"Zip file downloaded and saved to: {save_path}")
    return save_path
