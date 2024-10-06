"""main"""

from logging import config, getLogger
from pathlib import Path
from time import perf_counter, sleep

from tenacity import retry, stop_after_attempt, wait_random

from approved_npo_data.all_npo_data import get_all_npo_data_from_url
from approved_npo_data.approved_npo_data import get_approved_npo_data
from approved_npo_data.config import MAX_ITEMS_TO_PROCESS, SCRAPING_DELAY_SECONDS
from approved_npo_data.csv.csv_row import AllNpoDataRow, ApprovedNpoRow, OutputApprovedNpoRow
from approved_npo_data.scraping.npoportal_detail.viewing_documents import scrape_viewing_documents
from approved_npo_data.scraping.npoportal_detail.viewing_documents_model import (
    FinancialActivityReport,
)
from approved_npo_data.util.date_format import simple_format_time
from approved_npo_data.util.enumerate import controlled_enumerate
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


def createOutputApprovedNpoRow(
    approved_npo_row: ApprovedNpoRow, npo_data: AllNpoDataRow, detail_page_data: list[str]
) -> OutputApprovedNpoRow:
    """出力データを作成する"""
    return OutputApprovedNpoRow(
        *approved_npo_row.getValues(), *npo_data.getValues(), *detail_page_data
    )


def main():
    """main"""
    logger.info("start main")
    logger.info("start get approved_npo_data")
    approved_npo_data = get_approved_npo_data()
    logger.info(f"end get approved_npo_data. {len(approved_npo_data)=}")

    logger.info("start save approved_npo_data")
    csv_file_path = get_output_path(BASE_PATH, "approved_npo_data")
    save_csv(approved_npo_data, csv_file_path)
    logger.info(f"end save approved_npo_data {csv_file_path=}")

    logger.info("start all npo data")
    all_npo_data = get_all_npo_data_from_url()
    logger.info(f"end all npo data {len(all_npo_data)=}")

    logger.info("start merge data")

    output_data = []
    not_in_approve_npo = []

    for _, approved_npo_row in controlled_enumerate(
        approved_npo_data, log_interval=10, max_items=MAX_ITEMS_TO_PROCESS
    ):
        associate_name = approved_npo_row.corporation_name

        def getNpoDataRow(associate_name: str) -> AllNpoDataRow:
            key = standardize_text_for_key(associate_name)
            if key not in all_npo_data:
                logger.info(f"{associate_name} は全NPO法人情報に存在しません。")
                not_in_approve_npo.append(associate_name)
                return AllNpoDataRow.emptyInstance()
            return all_npo_data[key]

        npoData = getNpoDataRow(associate_name)
        url = npoData.corporate_information_url
        # TODO: 詳細ページ情報
        detail_page_data = ["", ""]
        if url:
            try:
                # URLが存在する場合には詳細ページからスクレイピングを行う
                year, urls = get_viewing_documents(url)
                detail_page_data = [year, urls]

                # スクレイピングの負荷を考慮してスリープを入れる
                sleep(SCRAPING_DELAY_SECONDS)
            except Exception as e:
                logger.error(f"{associate_name} のスクレイピングに失敗しました。{url} {e}")
        outputApprovedNpoRow = createOutputApprovedNpoRow(
            approved_npo_row, npoData, detail_page_data
        )
        output_data.append(outputApprovedNpoRow)
    logger.info(f"end merge data {len(output_data)=}, {len(not_in_approve_npo)=}")

    logger.info("start save output data")
    output_csv_path = get_output_path(BASE_PATH)
    save_csv(output_data, output_csv_path)
    logger.info(f"end save output data {output_csv_path=}")

    logger.info("end main")


if __name__ == "__main__":
    start = perf_counter()
    main()
    end = perf_counter()
    logger.info(f"経過時間: {simple_format_time(end - start)}")
