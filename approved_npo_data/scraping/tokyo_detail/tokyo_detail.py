"""東京都の法人・団体情報をスクレイピングしてクラスに格納するスクリプト"""

from logging import getLogger
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup

from approved_npo_data.scraping.document import LinkDocument
from approved_npo_data.scraping.tokyo_detail.information_model import BasicInformation
from approved_npo_data.util.scraping import scrape

logger = getLogger(__name__)


def scrape_table_to_dict(details_section: BeautifulSoup) -> dict[str, str]:
    """スクレイピング対象のテーブルを辞書形式に変換"""

    def f(dt):
        key = dt.text.strip()
        dd = dt.find_next("dd")
        value = dd.text.strip() if dd else ""
        return key, value

    return {k: v for k, v in (f(dt) for dt in details_section.find_all("dt"))}


def extract_documents(details_section: BeautifulSoup, base_url: str) -> list[LinkDocument]:
    """閲覧書類のリストを取得し、絶対URLに変換"""
    links = details_section.find_all("a", href=True)
    return [
        LinkDocument(
            title=link.text.strip(),
            url=urljoin(base_url, link["href"].strip()),
        )
        for link in links
    ]


def create_basic_information(details_section: BeautifulSoup, base_url: str) -> BasicInformation:
    """辞書データを使用して BasicInformation インスタンスを作成"""
    # テーブルデータを辞書形式に変換
    table_data = scrape_table_to_dict(details_section)

    # 閲覧書類を追加で処理
    table_data["閲覧書類"] = extract_documents(details_section, base_url)  # type: ignore

    # BasicInformation のインスタンスを生成
    return BasicInformation.from_dict(table_data)


def is_tokyo_detail_url(url: str) -> bool:
    """東京都の法人・団体情報詳細ページのURLかどうかを判定"""
    base_host = "www.seikatubunka.metro.tokyo.lg.jp"
    base_scheme = "https"

    if not url:
        return False
    try:
        parsed_url = urlparse(url)
        return parsed_url.scheme == base_scheme and parsed_url.netloc == base_host
    except ValueError:
        # URLが無効な場合はFalseを返す
        return False


def scrape_tokyo_detail(url: str, associate_name="") -> BasicInformation:
    """東京都の法人・団体情報詳細を取得"""
    # url = "https://www.seikatubunka.metro.tokyo.lg.jp/houjin/npo_houjin/list/ledger/0007570.html"
    empty_data = BasicInformation.emptyInstance()
    if not is_tokyo_detail_url(url):
        return empty_data
    try:
        # HTMLの取得と解析
        soup = scrape(url)

        # 法人・団体情報詳細セクションの取得
        details_section = soup.find("dl", class_="Corp_detail_dl")
        basic_info = create_basic_information(details_section, url)  # type: ignore
        return basic_info
    except Exception as e:
        base_message = "東京都の法人・団体情報詳細ページのスクレイピングに失敗しました。"
        logger.error(f"{base_message} {associate_name=}, {url=}, {e=}")
        return empty_data
