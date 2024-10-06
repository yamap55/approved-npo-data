"""main"""

from logging import config, getLogger
from pathlib import Path
from time import perf_counter, sleep

from tenacity import retry, stop_after_attempt, wait_random

from approved_npo_data.all_npo_data import get_all_npo_data_from_url
from approved_npo_data.approved_npo_data import (
    CSV_HEADER,
    get_approved_npo_data,
)
from approved_npo_data.config import MAX_ITEMS_TO_PROCESS, SCRAPING_DELAY_SECONDS
from approved_npo_data.scraping.npoportal_detail.viewing_documents import scrape_viewing_documents
from approved_npo_data.scraping.npoportal_detail.viewing_documents_model import (
    FinancialActivityReport,
)
from approved_npo_data.util.date_format import simple_format_time
from approved_npo_data.util.file_operations import get_output_path, save_csv
from approved_npo_data.util.text_format import standardize_text_for_key

config.fileConfig("logging.conf", disable_existing_loggers=False)
logger = getLogger(__name__)

BASE_PATH = Path(".")
BASE_PATH.mkdir(parents=True, exist_ok=True)


# 件数が多いからか割と失敗するためリトライを設定している
@retry(stop=stop_after_attempt(3), wait=wait_random(min=1, max=10))
def get_viewing_documents(url: str) -> tuple[str, str]:
    """法人情報のURLから最新年度の財務活動報告書のURLを取得する"""
    viewing_documents = scrape_viewing_documents(url)
    financial_activity_report = viewing_documents.financial_activity_reports.get_latest_report()

    def f(report: FinancialActivityReport):
        urls = "\n".join(d.url for d in report.documents)
        return str(report.year), urls

    year, urls = f(financial_activity_report) if financial_activity_report else ("", "")
    return year, urls


def main():
    """main"""
    logger.info("start main")
    logger.info("start get approved_npo_data")
    approved_npo_data = get_approved_npo_data()
    logger.info(f"end get approved_npo_data. {len(approved_npo_data)=}")

    logger.info("start save approved_npo_data")
    csv_file_path = get_output_path(BASE_PATH, "approved_npo_data")
    save_csv(approved_npo_data, CSV_HEADER, csv_file_path)
    logger.info(f"end save approved_npo_data {csv_file_path=}")

    logger.info("start all npo data")
    all_npo_data, all_npo_data_header = get_all_npo_data_from_url()
    logger.info(f"end all npo data {len(all_npo_data)=}")

    logger.info("start merge data")
    document_urls_header = ["ドキュメント最新年度", "ドキュメントURL"]
    output_csv_header = CSV_HEADER + all_npo_data_header + document_urls_header

    output_data = []
    not_in_approve_npo = []

    # 全NPO法人情報に存在しない場合のデータ
    EMPTY_NPO_DATA = ["" for _ in all_npo_data_header]
    EMPTY_DOCUMENT_URLS_DATA = ["" for _ in document_urls_header]

    all_size = len(approved_npo_data)
    for i, approved_npo_row in enumerate(approved_npo_data):
        if i == MAX_ITEMS_TO_PROCESS:
            break
        if i % 10 == 0:
            logger.info(f"{i + 1}/{all_size}")
        associate_name = approved_npo_row[6]
        key = standardize_text_for_key(associate_name)
        row = EMPTY_NPO_DATA + EMPTY_DOCUMENT_URLS_DATA
        if key not in all_npo_data:
            logger.info(f"{associate_name} は全NPO法人情報に存在しません。")
            not_in_approve_npo.append(associate_name)
        else:
            associate_data = all_npo_data[key]
            url = associate_data["法人情報URL"]
            document_urls = EMPTY_DOCUMENT_URLS_DATA
            if url:
                try:
                    # URLが存在する場合には詳細ページからスクレイピングを行う
                    year, urls = get_viewing_documents(url)
                    document_urls = [year, urls]

                    # スクレイピングの負荷を考慮してスリープを入れる
                    sleep(SCRAPING_DELAY_SECONDS)
                except Exception as e:
                    logger.error(f"{associate_name} のスクレイピングに失敗しました。{url} {e}")

            row = list(associate_data.values()) + document_urls
        output_data.append(approved_npo_row + row)
    logger.info(f"end merge data {len(output_data)=}, {len(not_in_approve_npo)=}")

    logger.info("start save output data")
    output_csv_path = get_output_path(BASE_PATH)
    save_csv(output_data, output_csv_header, output_csv_path)
    logger.info(f"end save output data {output_csv_path=}")

    logger.info("end main")


if __name__ == "__main__":
    start = perf_counter()
    main()
    end = perf_counter()
    logger.info(f"経過時間: {simple_format_time(end - start)}")
