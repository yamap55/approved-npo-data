"""NPOポータルの詳細ページのデータを取得する"""

from approved_npo_data.scraping.npoportal_detail.information import scrape_npo_information
from approved_npo_data.scraping.npoportal_detail.viewing_documents import scrape_viewing_documents
from approved_npo_data.scraping.npoportal_detail.viewing_documents_model import (
    FinancialActivityReport,
)
from approved_npo_data.util.scraping import scrape


def get_detail_data(url: str) -> list[str]:
    """詳細ページのデータを取得する"""
    soup = scrape(url)
    viewing_documents = scrape_viewing_documents(soup)
    information = scrape_npo_information(soup)
    financial_activity_report = viewing_documents.financial_activity_reports.get_latest_report()

    def f(report: FinancialActivityReport):
        urls = "\n".join(f"{d.title}: {d.url}" for d in report.documents)
        return str(report.year), urls

    information_row = information.to_csv_row()
    year, urls = f(financial_activity_report) if financial_activity_report else ("", "")
    # TODO: 本来はdataclassを返すべきだがとりあえず値だけListで返す
    return information_row + [year, urls]
