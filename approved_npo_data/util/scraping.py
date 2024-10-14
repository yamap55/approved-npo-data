"""スクレイピング関連のユーティリティ"""

import requests
from bs4 import BeautifulSoup
from tenacity import retry, stop_after_attempt, wait_random


# リトライ設定
@retry(stop=stop_after_attempt(3), wait=wait_random(min=1, max=10))
def scrape(url: str):
    """渡されたURLからスクレイピングする"""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        raise ValueError(f"URLの取得に失敗しました: {url}. エラー: {e}") from e

    # BeautifulSoupでHTMLを解析
    return BeautifulSoup(response.content, "html.parser")
