"""東京都の法人・団体情報を保持するモデル"""

from dataclasses import dataclass, field
from logging import getLogger

from approved_npo_data.scraping.document import LinkDocument
from approved_npo_data.util.model_base import ModelBase

logger = getLogger(__name__)


@dataclass(frozen=True)
class BasicInformation(ModelBase):
    """東京都の法人・団体情報"""

    corporate_number: str = field(default="", metadata={"key": "法人番号"})
    """法人番号"""

    approval_date: str = field(default="", metadata={"key": "認証日"})
    """認証日"""

    corporate_name: str = field(default="", metadata={"key": "法人・団体名称"})
    """法人・団体名称"""

    corporate_name_kana: str = field(default="", metadata={"key": "法人・団体名称カナ"})
    """法人・団体名称カナ"""

    main_office_address: str = field(default="", metadata={"key": "主たる事務所の所在地"})
    """主たる事務所の所在地"""

    secondary_office_address: str = field(
        default="", metadata={"key": "従たる事務所の所在地", "optional": True}
    )
    """
    従たる事務所の所在地

    ※存在しない場合があるため、optional=Trueと指定している
    """

    representative_name: str = field(default="", metadata={"key": "代表者氏名"})
    """代表者氏名"""

    articles_of_incorporation_purpose: str = field(
        default="", metadata={"key": "定款に記載された目的"}
    )
    """定款に記載された目的"""

    activity_fields: str = field(default="", metadata={"key": "活動分野"})
    """活動分野"""

    phone_number: str = field(default="", metadata={"key": "電話番号"})
    """電話番号"""

    fiscal_year: str = field(default="", metadata={"key": "事業年度"})
    """事業年度"""

    approval_status: str = field(default="", metadata={"key": "認定状態"})
    """認定状態"""

    approval_date_for_exception: str = field(
        default="", metadata={"key": "認定（特例認定）日", "optional": True}
    )
    """
    認定（特例認定）日

    ※存在しない場合があるため、optional=Trueと指定している
    """

    validity_period: str = field(default="", metadata={"key": "有効期間"})
    """有効期間"""

    dissolution_date: str = field(default="", metadata={"key": "解散日", "optional": True})
    """
    解散日

    ※存在しない場合があるため、optional=Trueと指定している
    """

    dissolution_reason: str = field(default="", metadata={"key": "解散理由", "optional": True})
    """
    解散理由

    ※存在しない場合があるため、optional=Trueと指定している
    """

    documents: list[LinkDocument] = field(default_factory=list, metadata={"key": "閲覧書類"})
    """閲覧書類"""

    def to_csv_field_documents(self):
        """閲覧書類をCSV用のフィールドに変換"""
        return "\n".join([f"{doc.title}: {doc.url}" for doc in self.documents])
