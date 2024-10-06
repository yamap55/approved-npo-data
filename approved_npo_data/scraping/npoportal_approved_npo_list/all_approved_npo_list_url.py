"""認定NPO法人のデータのURLを取得する"""

import re

import requests
from bs4 import BeautifulSoup

ALL_APPROVED_NPO_LIST_URL = "https://www.npo-homepage.go.jp/npoportal/certification"
APPROVED_NPO_DATA_URL_PATTERN = re.compile(r"全国 所轄庁認定・特例認定NPO法人名簿")


def get_approved_npo_data_url() -> str:
    """認定NPO法人のデータのURLを取得する"""
    try:
        response = requests.get(ALL_APPROVED_NPO_LIST_URL, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        raise ValueError(
            f"URLの取得に失敗しました: {ALL_APPROVED_NPO_LIST_URL}. エラー: {e}"
        ) from e

    soup = BeautifulSoup(response.content, "html.parser")
    link = soup.find("a", href=True, string=APPROVED_NPO_DATA_URL_PATTERN)

    return link["href"]  # type: ignore
