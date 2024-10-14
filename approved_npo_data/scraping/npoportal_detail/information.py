"""NPO法人ポータルの詳細ページから基本情報をスクレイピングする"""

import re

from bs4 import BeautifulSoup

from approved_npo_data.scraping.npoportal_detail.Information_model import Information
from approved_npo_data.util.url import extract_embedded_url


def clean_text(text: str) -> str:
    """テキストを整形する"""
    # 改行と連続するスペースを単一のスペースに変換
    return re.sub(r"\s+", " ", text.strip())


def extract_table_data(soup: BeautifulSoup) -> dict[str, str]:
    """
    BeautifulSoupオブジェクトから基本情報を辞書として抽出する。
    """
    table = soup.find("table", summary="基本情報")
    if not table:
        raise ValueError("基本情報のテーブルが見つかりませんでした。")
    data = {}

    if table:
        for row in table.find_all("tr"):  # type: ignore
            th = row.find("th")
            td = row.find("td")
            if th and td:
                key = clean_text(th.get_text(strip=True))
                # リンクがある場合はhref属性を取得し、リンクがない場合はテキストを取得
                if a_tag := td.find("a"):
                    value = extract_embedded_url(a_tag["href"])
                else:
                    value = clean_text(td.get_text())
                data[key] = value

    return data


def scrape_npo_information(soup: BeautifulSoup) -> Information:
    """
    NPOの詳細情報をスクレイピングしてNPOInformationを生成する。
    """
    # テーブルデータを辞書として抽出
    data_dict = extract_table_data(soup)

    # 抽出したデータを元にNPOInformationインスタンスを生成
    information = Information.from_dict(data_dict)

    return information
