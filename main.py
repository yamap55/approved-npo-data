"""main"""

from logging import config, getLogger
from pathlib import Path
from time import perf_counter

from approved_npo_data.all_npo_data import get_all_npo_data_from_url
from approved_npo_data.approved_npo_data import (
    CSV_HEADER,
    get_approved_npo_data,
)
from approved_npo_data.util.date_format import simple_format_time
from approved_npo_data.util.file_operations import get_output_path, save_csv
from approved_npo_data.util.text_format import standardize_text_for_key

config.fileConfig("logging.conf", disable_existing_loggers=False)
logger = getLogger(__name__)

BASE_PATH = Path(".")
BASE_PATH.mkdir(parents=True, exist_ok=True)


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
    all_npo_data, header = get_all_npo_data_from_url()
    logger.info(f"end all npo data {len(all_npo_data)=}")

    logger.info("start merge data")
    output_csv_header = CSV_HEADER + header

    output_data = []
    not_in_approve_npo = []
    EMPTY_NPO_DATA = ["" for _ in header]

    for approved_npo_row in approved_npo_data:
        associate_name = approved_npo_row[6]
        key = standardize_text_for_key(associate_name)
        row = EMPTY_NPO_DATA
        if key not in all_npo_data:
            logger.info(f"{associate_name} は全NPO法人情報に存在しません。")
            not_in_approve_npo.append(associate_name)
        else:
            associate_data = all_npo_data[key]
            row = list(associate_data.values())
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
