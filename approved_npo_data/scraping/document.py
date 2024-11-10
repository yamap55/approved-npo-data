"""文書データのモデル"""

from dataclasses import dataclass

from approved_npo_data.util.model_base import ModelBase


@dataclass(frozen=True)
class LinkDocument(ModelBase):
    """リンク付きの文書"""

    title: str
    url: str


@dataclass(frozen=True)
class NonLinkDocument(ModelBase):
    """リンクなしの文書"""

    value: str
