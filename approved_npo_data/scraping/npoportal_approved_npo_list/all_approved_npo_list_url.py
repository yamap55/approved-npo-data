"""認定NPO法人のデータのURLを取得する"""

import re

from approved_npo_data.util.scraping import scrape

ALL_APPROVED_NPO_LIST_URL = "https://www.npo-homepage.go.jp/npoportal/certification"
APPROVED_NPO_DATA_URL_PATTERN = re.compile(r"全国 所轄庁認定・特例認定NPO法人名簿")


def get_approved_npo_data_url() -> str:
    """認定NPO法人のデータのURLを取得する"""
    soup = scrape(ALL_APPROVED_NPO_LIST_URL)
    link = soup.find("a", href=True, string=APPROVED_NPO_DATA_URL_PATTERN)

    return link["href"]  # type: ignore
