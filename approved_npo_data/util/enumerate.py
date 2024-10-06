"""拡張enumerate"""

from collections.abc import Iterator, Sequence
from logging import getLogger
from typing import TypeVar

logger = getLogger(__name__)


T = TypeVar("T")


def controlled_enumerate(
    data: Sequence[T], log_interval=1, max_items=None
) -> Iterator[tuple[int, T]]:
    """enumerate()の拡張版"""
    all_size = len(data)
    for i, d in enumerate(data):
        if max_items is not None and i >= max_items:
            break
        if i % log_interval == 0:
            logger.info(f"{i + 1}/{all_size}")

        yield i, d
