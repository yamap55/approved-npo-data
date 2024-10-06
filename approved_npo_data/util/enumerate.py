"""拡張enumerate"""

from logging import getLogger

logger = getLogger(__name__)


def controlled_enumerate(data, log_interval=1, max_items=None):
    """enumerate()の拡張版"""
    all_size = len(data)
    for i, d in enumerate(data):
        if max_items is not None and i >= max_items:
            break
        if i % log_interval == 0:
            logger.info(f"{i + 1}/{all_size}")

        yield i, d
