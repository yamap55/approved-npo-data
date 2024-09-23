"""main"""

from logging import config

from approved_npo_data.huga import Huga

config.fileConfig("logging.conf", disable_existing_loggers=False)

if __name__ == "__main__":
    Huga().piyo()
