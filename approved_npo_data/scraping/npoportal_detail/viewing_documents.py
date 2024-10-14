"""NPO法人ポータルの詳細ページから閲覧書類等をスクレイピングする"""

import re

from bs4 import BeautifulSoup

from approved_npo_data.scraping.npoportal_detail.viewing_documents_model import (
    Bylaws,
    FinancialActivityReport,
    FinancialActivityReports,
    LinkDocument,
    NonLinkDocument,
    OtherReport,
    ViewingDocuments,
)


def is_nendo_format(text: str) -> bool:
    """年度のフォーマットかを判定する"""
    pattern = r"^\d+年度$"
    return bool(re.match(pattern, text))


def is_bylaws(text: str) -> bool:
    """定款のカテゴリかを判定する"""
    return "定款" in text


def create_report_from_category(
    category: str, td
) -> tuple[str, FinancialActivityReport | Bylaws | OtherReport]:
    """カテゴリから報告書を作成する"""
    # 年度のカテゴリかを判別
    if is_nendo_format(category):
        year = int(re.findall(r"\d+", category)[0])
        documents = [
            LinkDocument(title=a.get_text(strip=True), url=a["href"]) for a in td.find_all("a")
        ]
        report = FinancialActivityReport(category=category, year=year, documents=documents)
        return "financial_activity_report", report

    # 定款カテゴリかを判別
    elif is_bylaws(category):
        document_link = td.find("a")
        if document_link:
            doc = LinkDocument(title=document_link.get_text(strip=True), url=document_link["href"])
        else:
            doc = NonLinkDocument(value=td.get_text(strip=True))
        return "bylaws", Bylaws(category=category, document=doc)

    # その他のレポート
    else:
        return "other", OtherReport(category=category, value=td.get_text(strip=True))


def scrape_viewing_documents(soup: BeautifulSoup) -> ViewingDocuments:
    """閲覧書類等をスクレイピングする"""
    # 「閲覧書類等」のテーブルを探す
    table = soup.find("table", {"summary": "閲覧書類"})
    if not table:
        raise ValueError("閲覧書類等のテーブルが見つかりませんでした。")

    bylaws = None
    other_reports = []
    financial_reports = FinancialActivityReports(category="Financial Reports")

    rows = table.find_all("tr")  # type: ignore

    for row in rows:
        th = row.find("th")
        td = row.find("td")

        if th and td:
            category: str = th.get_text(strip=True)
            category_type, data = create_report_from_category(category, td)
            if category_type == "financial_activity_report":
                financial_reports.reports.append(data)  # type: ignore
            elif category_type == "bylaws":
                if bylaws:
                    raise ValueError("定款のカテゴリが複数存在します。")
                bylaws = data
            elif category_type == "other":
                other_reports.append(data)

    return ViewingDocuments(
        financial_activity_reports=financial_reports,
        bylaws=bylaws,  # type: ignore
        other=other_reports,
    )
