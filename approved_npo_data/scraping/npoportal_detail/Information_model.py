"""NPOポータルの詳細ページから取得したNPO情報を保持するモデル"""

from dataclasses import dataclass, field
from logging import getLogger

from approved_npo_data.util.model_base import ModelBase

logger = getLogger(__name__)


@dataclass(frozen=True)
class Information(ModelBase):
    """Npo情報"""

    jurisdiction: str = field(default="", metadata={"key": "所轄庁"})
    """所轄庁"""

    delegated_municipality: str = field(default="", metadata={"key": "権限移譲先市町村"})
    """権限移譲先市町村"""

    corporate_name: str = field(default="", metadata={"key": "法人名称"})
    """法人名称"""

    corporate_name_kana: str = field(default="", metadata={"key": "法人名称（フリガナ）"})
    """法人名称（フリガナ）"""

    main_office_postal_code: str = field(default="", metadata={"key": "主たる事業所の郵便番号"})
    """主たる事業所の郵便番号"""

    main_office_address: str = field(default="", metadata={"key": "主たる事務所の所在地"})
    """主たる事務所の所在地"""

    secondary_office_address: str = field(default="", metadata={"key": "従たる事務所の所在地"})
    """従たる事務所の所在地"""

    representative_name: str = field(default="", metadata={"key": "代表者氏名"})
    """代表者氏名"""

    representative_name_kana: str = field(default="", metadata={"key": "代表者氏名（フリガナ）"})
    """代表者氏名（フリガナ）"""

    establishment_approval_date: str = field(default="", metadata={"key": "設立認証年月日"})
    """設立認証年月日"""

    establishment_date: str = field(default="", metadata={"key": "設立年月日"})
    """設立年月日"""

    articles_of_incorporation_purpose: str = field(
        default="", metadata={"key": "定款に記載された目的"}
    )
    """定款に記載された目的"""

    activity_fields: str = field(default="", metadata={"key": "活動分野"})
    """活動分野"""

    specified_nonprofit_activities: str = field(
        default="", metadata={"key": "特定非営利活動に係る事業"}
    )
    """特定非営利活動に係る事業"""

    other_business: str = field(default="", metadata={"key": "その他の事業"})
    """その他の事業"""

    fiscal_year_start: str = field(default="", metadata={"key": "事業年度開始日"})
    """事業年度開始日"""

    fiscal_year_end: str = field(default="", metadata={"key": "事業年度終了日"})
    """事業年度終了日"""

    corporate_number: str = field(default="", metadata={"key": "法人番号"})
    """法人番号"""

    approval_status: str = field(default="", metadata={"key": "認定", "optional": True})
    """
    認定

    ※存在しない場合があるため、optional=Trueと指定している（条件不明）
    """

    jurisdiction_public_site: str = field(
        default="", metadata={"key": "所轄庁の情報公開サイト", "optional": True}
    )
    """
    所轄庁の情報公開サイト

    ※存在しない場合があるため、optional=Trueと指定している（東京都のみ？）
    """

    dissolution_date: str = field(default="", metadata={"key": "解散日", "optional": True})
    """
    解散日

    ※存在しない場合があるため、optional=Trueと指定している（解散している場合か？）
    """

    dissolution_reason: str = field(default="", metadata={"key": "解散理由", "optional": True})
    """
    解散理由

    ※存在しない場合があるため、optional=Trueと指定している（解散している場合か？）
    """

    individual_approval_by_ordinance: str = field(
        default="", metadata={"key": "条例による個別認定", "optional": True}
    )
    """
    条例による個別認定

    ※存在しない場合があるため、optional=Trueと指定している（条件不明）
    """
