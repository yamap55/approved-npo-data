"""NPOポータルの詳細ページから取得したNPO情報を保持するモデル"""

from dataclasses import dataclass, field, fields
from logging import getLogger

logger = getLogger(__name__)


@dataclass(frozen=True)
class Information:
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

    approval_status: str = field(default="", metadata={"key": "認定"})
    """認定"""

    jurisdiction_public_site: str = field(
        default="", metadata={"key": "所轄庁の情報公開サイト", "optional": True}
    )
    """
    所轄庁の情報公開サイト

    ※存在しない場合があるため、optional=Trueと指定している（東京都のみ？）
    """

    @classmethod
    def get_field_mapping(cls) -> dict[str, str]:
        """
        メタデータを使用してフィールド名とキーのマッピングを生成する。

        Returns:
            Dict[str, str]: キーとフィールド名の辞書。
        """
        return {
            field.metadata["key"]: field.name for field in fields(cls) if "key" in field.metadata
        }

    @classmethod
    def _validate_data_keys(cls, data: dict[str, str]) -> None:
        field_mapping = cls.get_field_mapping()
        data_keys = set(data.keys())
        field_keys = set(field_mapping.keys())

        # チェック部分
        unknown_keys = data_keys - field_keys
        if unknown_keys:
            logger.warning(f"未知のキーが存在します: {', '.join(unknown_keys)}")

        missing_keys = {
            key
            for key in field_keys - data_keys
            # optional=Trueのフィールドは存在しない場合を許容する
            if not any(f.metadata.get("optional") for f in fields(cls) if f.metadata["key"] == key)
        }
        if missing_keys:
            logger.warning(f"必要なキーが存在しませんでした: {', '.join(missing_keys)}")

    @classmethod
    def from_dict(cls, data: dict[str, str]) -> "Information":
        """
        辞書からデータを設定して、AdministrativeDataのインスタンスを生成する。

        Args:
            data (Dict[str, str]): キーと値の辞書。

        Returns:
            AdministrativeData: 抽出したデータを持つオブジェクト。
        """
        field_mapping = cls.get_field_mapping()
        cls._validate_data_keys(data)

        # データを初期化時に渡すためにフィールド名と対応する値を辞書としてまとめる
        init_values = {
            field_mapping[key]: value for key, value in data.items() if key in field_mapping
        }
        return cls(**init_values)

    @classmethod
    def get_csv_header(cls) -> list[str]:
        """CSV出力用のヘッダーを日本語で取得"""
        return [field.metadata["key"] for field in fields(cls) if "key" in field.metadata]

    def to_csv_row(self) -> list[str]:
        """CSVの1行分のデータを取得"""
        return [getattr(self, field.name) for field in fields(self)]
