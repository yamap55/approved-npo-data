"""テキストフォーマットを扱う関数群"""

import re
import unicodedata

# 正規表現のパターンを事前にコンパイル
whitespace_pattern = re.compile(r"[\u3000\s\t]+")


def standardize_text_for_key(text: str) -> str:
    """Keyとして使用できるように文字列を標準化する"""
    # 全角英数字を半角英数字に変換
    text = unicodedata.normalize("NFKC", text)

    # 全角スペース、半角スペース、タブを除去
    text = whitespace_pattern.sub("", text)

    return text
