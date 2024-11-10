"""main"""

from logging import config, getLogger
from pathlib import Path
from time import perf_counter, sleep

from approved_npo_data.all_npo_data import get_all_npo_data_from_url
from approved_npo_data.approved_npo_data import get_approved_npo_data
from approved_npo_data.config import MAX_ITEMS_TO_PROCESS, SCRAPING_DELAY_SECONDS
from approved_npo_data.csv.csv_row import AllNpoDataRow, ApprovedNpoRow, OutputApprovedNpoRow
from approved_npo_data.scraping.npoportal_detail.npoportal_detail import get_detail_data
from approved_npo_data.scraping.tokyo_detail.information_model import BasicInformation
from approved_npo_data.scraping.tokyo_detail.tokyo_detail import scrape_tokyo_detail
from approved_npo_data.util.date_format import simple_format_time
from approved_npo_data.util.enumerate import controlled_enumerate
from approved_npo_data.util.file_operations import get_output_path, save_csv

config.fileConfig("logging.conf", disable_existing_loggers=False)
logger = getLogger(__name__)

BASE_PATH = Path(".")
BASE_PATH.mkdir(parents=True, exist_ok=True)


def createOutputApprovedNpoRow(
    approved_npo_row: ApprovedNpoRow,
    npo_data: AllNpoDataRow,
    detail_page_data: list[str],
    tokyo_detail: BasicInformation,
) -> OutputApprovedNpoRow:
    """出力データを作成する"""
    return OutputApprovedNpoRow(
        *approved_npo_row.to_csv_row(),
        *npo_data.to_csv_row(),
        *detail_page_data,
        *tokyo_detail.to_csv_row(),
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
        corporate_number = approved_npo_row.corporate_number

        def getNpoDataRow(associate_name: str, corporate_number: str) -> AllNpoDataRow:
            if corporate_number not in all_npo_data:
                logger.info(f"全NPO法人情報に存在しません。 {associate_name=}, {corporate_number=}")
                not_in_approve_npo.append(corporate_number)
                return AllNpoDataRow.emptyInstance()
            return all_npo_data[corporate_number]

        npoData = getNpoDataRow(associate_name, corporate_number)
        url = npoData.corporate_information_url

        # 詳細ページからスクレイピング
        information, detail_data = get_detail_data(url, associate_name)

        # 所轄庁の情報公開サイトからスクレイピング
        # 現在は東京のみ
        tokyo_detail = scrape_tokyo_detail(information.jurisdiction_public_site, associate_name)

        # スクレイピングの負荷を考慮してスリープを入れる
        sleep(SCRAPING_DELAY_SECONDS)
        outputApprovedNpoRow = createOutputApprovedNpoRow(
            approved_npo_row, npoData, detail_data, tokyo_detail
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
