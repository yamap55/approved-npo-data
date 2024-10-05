"""「閲覧書類等」部のデータ定義"""

from abc import ABC
from dataclasses import dataclass, field


@dataclass(frozen=True)
class LinkDocument:
    """リンク付きの文書"""

    title: str
    url: str


@dataclass(frozen=True)
class NonLinkDocument:
    """リンクなしの文書"""

    value: str


@dataclass(frozen=True)
class Report(ABC):
    """報告書"""

    category: str


@dataclass(frozen=True)
class Bylaws(Report):
    """定款"""

    document: LinkDocument | NonLinkDocument


@dataclass(frozen=True)
class OtherReport(Report, NonLinkDocument):
    """その他の報告書"""

    pass


@dataclass(frozen=True)
class FinancialActivityReport(Report):
    """財務系の報告書"""

    year: int
    documents: list[LinkDocument] = field(default_factory=list)


@dataclass(frozen=True)
class FinancialActivityReports(Report):
    """財務系の報告書群"""

    category = "Financial Reports"
    reports: list[FinancialActivityReport] = field(default_factory=list)

    def get_latest_report(self) -> FinancialActivityReport | None:
        """最新の報告書を取得する"""
        return max(self.reports, key=lambda x: x.year, default=None)


@dataclass(frozen=True)
class ViewingDocuments:
    """閲覧書類等"""

    financial_activity_reports: FinancialActivityReports
    bylaws: Bylaws | None
    other: list[OtherReport]
