"""日時関連の関数群"""


def simple_format_time(duration: int | float) -> str:
    """
    秒数をHH時間MM分SS秒にフォーマットする
    """
    hours, remainder = divmod(duration, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{int(hours)}時間{int(minutes)}分{int(seconds)}秒"
