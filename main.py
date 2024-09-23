"""main"""

from logging import config

from approved_npo_data.from_pdf.get_approved_npo_data import main

config.fileConfig("logging.conf", disable_existing_loggers=False)

if __name__ == "__main__":
    main()
