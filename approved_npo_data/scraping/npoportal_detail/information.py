"""NPO法人ポータルの詳細ページから基本情報をスクレイピングする"""

import re

import requests
from bs4 import BeautifulSoup

from approved_npo_data.scraping.npoportal_detail.Information_model import Information
from approved_npo_data.util.url import extract_embedded_url


def clean_text(text: str) -> str:
    """テキストを整形する"""
    # 改行と連続するスペースを単一のスペースに変換
    return re.sub(r"\s+", " ", text.strip())


def extract_table_data(soup: BeautifulSoup) -> dict[str, str]:
    """
    BeautifulSoupオブジェクトからテーブルデータを辞書として抽出する。

    Args:
        soup (BeautifulSoup): 行政入力情報を含むBeautifulSoupオブジェクト。

    Returns:
        Dict[str, str]: テーブルデータのキーと値の辞書。
    """
    table = soup.find("table", summary="基本情報")
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


def scrape_npo_information(detail_url: str) -> Information:
    """
    指定されたURLからNPOの詳細情報をスクレイピングしてNPOInformationを生成する。

    Args:
        detail_url (str): スクレイピングするNPO詳細ページのURL。

    Returns:
        NPOInformation: 取得したデータを元に生成されたNPOInformationインスタンス。
    """
    try:
        response = requests.get(detail_url, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        raise ValueError(f"URLの取得に失敗しました: {detail_url}. エラー: {e}") from e

    # BeautifulSoupでHTMLを解析
    soup = BeautifulSoup(response.content, "html.parser")

    # テーブルデータを辞書として抽出
    data_dict = extract_table_data(soup)

    # 抽出したデータを元にNPOInformationインスタンスを生成
    information = Information.from_dict(data_dict)

    return information
