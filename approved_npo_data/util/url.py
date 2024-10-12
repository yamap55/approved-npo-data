"""URLに関するユーティリティ関数"""

from urllib.parse import parse_qs, unquote, urlparse


def extract_embedded_url(url: str, param_name: str = "url") -> str:
    """URLに埋め込まれているURLを抽出する関数"""
    parsed_url = urlparse(url)

    query_params = parse_qs(parsed_url.query)
    embedded_url = query_params.get(param_name, [None])[0]

    if embedded_url:
        return unquote(embedded_url)
    else:
        return ""
