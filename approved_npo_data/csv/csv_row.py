"""CSVの行データを表すクラス群"""

from abc import ABC
from dataclasses import dataclass, field, fields
from typing import Self


@dataclass(frozen=True)
class CsvRow(ABC):  # noqa: B024
    """CSVの行データを表す抽象クラス"""

    @classmethod
    def emptyInstance(cls) -> Self:
        """
        空のインスタンスを返す

        NOTE: 現在の実装では、フィールドは全て文字列型であることを想定している
        正しくやるのであれば全てのフィールドにデフォルト値を設定するのが簡単か。
        """
        return cls(*["" for _ in fields(cls)])

    def getValues(self) -> list:
        """CSVの値を返す"""
        return [getattr(self, f.name) for f in fields(self)]

    @classmethod
    def getHeader(cls) -> list[str]:
        """CSVのヘッダを返す"""
        return [field.metadata["key"] for field in fields(cls) if "key" in field.metadata]

    def to_csv_row(self) -> list[str]:
        """CSVの1行分のデータを取得"""
        return [getattr(self, field.name) for field in fields(self)]


@dataclass(frozen=True)
class ApprovedNpoRow(CsvRow):
    """認定NPO法人のデータ"""

    control_code: str = field(default="", metadata={"key": "所轄庁コード"})
    """所轄庁コード"""

    control_office: str = field(default="", metadata={"key": "所轄庁"})
    """所轄庁"""

    corporate_number: str = field(default="", metadata={"key": "法人番号"})
    """法人番号"""

    approved: str = field(default="", metadata={"key": "認定"})
    """認定"""

    special_approved: str = field(default="", metadata={"key": "特例認定"})
    """特例認定"""

    update_application: str = field(default="", metadata={"key": "更新申請中"})
    """更新申請中"""

    corporation_name: str = field(default="", metadata={"key": "法人名"})
    """法人名"""

    head_office_address: str = field(default="", metadata={"key": "主たる事務所の所在地"})
    """主たる事務所の所在地"""

    representative_name: str = field(default="", metadata={"key": "代表者氏名"})
    """代表者氏名"""

    pst_relative_value: str = field(default="", metadata={"key": "PST基準 相対値"})
    """PST基準 相対値"""

    pst_absolute_value: str = field(default="", metadata={"key": "PST基準 絶対値"})
    """PST基準 絶対値"""

    pst_specified_by_law: str = field(default="", metadata={"key": "PST基準 条例指定"})
    """PST基準 条例指定"""

    pst_specified_by_law_local_government_name: str = field(
        default="", metadata={"key": "PST基準 条例指定 自治体名"}
    )
    """PST基準 条例指定 自治体名"""

    approved_validity_period_from: str = field(default="", metadata={"key": "認定有効期間 自"})
    """認定有効期間 自"""

    approved_validity_period_to: str = field(default="", metadata={"key": "認定有効期間 至"})
    """認定有効期間 至"""

    special_approved_validity_period_from: str = field(
        default="", metadata={"key": "特例認定有効期間 自"}
    )
    """特例認定有効期間 自"""

    special_approved_validity_period_to: str = field(
        default="", metadata={"key": "特例認定有効期間 至"}
    )
    """特例認定有効期間 至"""


@dataclass(frozen=True)
class AllNpoDataRow(CsvRow):
    """全NPO法人のデータ"""

    corporation_name: str = field(default="", metadata={"key": "法人名称"})
    """法人名称"""

    corporation_name_kana: str = field(default="", metadata={"key": "法人名称カナ"})
    """法人名称カナ"""

    control_office: str = field(default="", metadata={"key": "所轄庁"})
    """所轄庁"""

    delegated_municipality: str = field(default="", metadata={"key": "権限移譲先市町村"})
    """権限移譲先市町村"""

    head_office_address: str = field(default="", metadata={"key": "主たる事務所の所在地"})
    """主たる事務所の所在地"""

    head_office_postal_code: str = field(default="", metadata={"key": "主たる事業所の郵便番号"})
    """主たる事業所の郵便番号"""

    branch_office_address: str = field(default="", metadata={"key": "従たる事務所の所在地"})
    """従たる事務所の所在地"""

    representative_name: str = field(default="", metadata={"key": "代表者氏名"})
    """代表者氏名"""

    representative_name_kana: str = field(default="", metadata={"key": "団体代表者名（フリガナ）"})
    """団体代表者名（フリガナ）"""

    corporate_establishment_certification_date: str = field(
        default="", metadata={"key": "法人設立認証年月日"}
    )
    """法人設立認証年月日"""

    establishment_date: str = field(default="", metadata={"key": "設立年月日"})
    """設立年月日"""

    purpose_described_in_the_articles: str = field(
        default="", metadata={"key": "定款に記載された目的"}
    )
    """定款に記載された目的"""

    activity_area_1: str = field(default="", metadata={"key": "活動分野１"})
    """活動分野１"""

    activity_area_2: str = field(default="", metadata={"key": "活動分野２"})
    """活動分野２"""

    activity_area_3: str = field(default="", metadata={"key": "活動分野３"})
    """活動分野３"""

    activity_area_4: str = field(default="", metadata={"key": "活動分野４"})
    """活動分野４"""

    activity_area_5: str = field(default="", metadata={"key": "活動分野５"})
    """活動分野５"""

    activity_area_6: str = field(default="", metadata={"key": "活動分野６"})
    """活動分野６"""

    activity_area_7: str = field(default="", metadata={"key": "活動分野７"})
    """活動分野７"""

    activity_area_8: str = field(default="", metadata={"key": "活動分野８"})
    """活動分野８"""

    activity_area_9: str = field(default="", metadata={"key": "活動分野９"})
    """活動分野９"""

    activity_area_10: str = field(default="", metadata={"key": "活動分野１０"})
    """活動分野１０"""

    activity_area_11: str = field(default="", metadata={"key": "活動分野１１"})
    """活動分野１１"""

    activity_area_12: str = field(default="", metadata={"key": "活動分野１２"})
    """活動分野１２"""

    activity_area_13: str = field(default="", metadata={"key": "活動分野１３"})
    """活動分野１３"""

    activity_area_14: str = field(default="", metadata={"key": "活動分野１４"})
    """活動分野１４"""

    activity_area_15: str = field(default="", metadata={"key": "活動分野１５"})
    """活動分野１５"""

    activity_area_16: str = field(default="", metadata={"key": "活動分野１６"})
    """活動分野１６"""

    activity_area_17: str = field(default="", metadata={"key": "活動分野１７"})
    """活動分野１７"""

    activity_area_18: str = field(default="", metadata={"key": "活動分野１８"})
    """活動分野１８"""

    activity_area_19: str = field(default="", metadata={"key": "活動分野１９"})
    """活動分野１９"""

    activity_area_20: str = field(default="", metadata={"key": "活動分野２０"})
    """活動分野２０"""

    approved_1: str = field(default="", metadata={"key": "認定（認定・特例認定１）"})
    """認定（認定・特例認定１）"""

    approved_2: str = field(default="", metadata={"key": "認定（認定・特例認定２）"})
    """認定（認定・特例認定２）"""

    approved_3: str = field(default="", metadata={"key": "認定（認定・特例認定３）"})
    """認定（認定・特例認定３）"""

    approved_4: str = field(default="", metadata={"key": "認定（認定・特例認定４）"})
    """認定（認定・特例認定４）"""

    pst_standard_1: str = field(default="", metadata={"key": "認定（PST基準１）"})
    """認定（PST基準１）"""

    pst_standard_2: str = field(default="", metadata={"key": "認定（PST基準２）"})
    """認定（PST基準２）"""

    pst_standard_3: str = field(default="", metadata={"key": "認定（PST基準３）"})
    """認定（PST基準３）"""

    pst_standard_specified_by_law: str = field(
        default="", metadata={"key": "認定（PST基準 条例指定（都道府県及び市区町村名））"}
    )
    """認定（PST基準 条例指定（都道府県及び市区町村名））"""

    approved_start_date: str = field(default="", metadata={"key": "認定（認定開始日）"})
    """認定（認定開始日）"""

    approved_expiration_date: str = field(default="", metadata={"key": "認定（認定満了日）"})
    """認定（認定満了日）"""

    approved_cancellation_date: str = field(default="", metadata={"key": "認定（認定取消日）"})
    """認定（認定取消日）"""

    special_approved_date: str = field(default="", metadata={"key": "認定（特例認定年月日）"})
    """認定（特例認定年月日）"""

    special_approved_expiration_date: str = field(
        default="", metadata={"key": "認定（特例認定満了日）"}
    )
    """認定（特例認定満了日）"""

    special_approved_cancellation_date: str = field(
        default="", metadata={"key": "認定（特例認定取消日）"}
    )
    """認定（特例認定取消日）"""

    supervision_information: str = field(default="", metadata={"key": "監督情報"})
    """監督情報"""

    dissolution_information: str = field(default="", metadata={"key": "解散情報"})
    """解散情報"""

    corporate_information_url: str = field(default="", metadata={"key": "法人情報URL"})
    """法人情報URL"""

    corporate_number: str = field(default="", metadata={"key": "法人番号"})
    """法人番号"""

    individual_specified_by_law_flag: str = field(
        default="", metadata={"key": "条例個別指定フラグ"}
    )
    """条例個別指定フラグ"""

    specific_non_profit_activities: str = field(
        default="", metadata={"key": "特定非営利活動に係る事業"}
    )
    """特定非営利活動に係る事業"""

    other_business: str = field(default="", metadata={"key": "その他の事業"})
    """その他の事業"""

    business_year_start_date: str = field(default="", metadata={"key": "事業年度開始日"})
    """事業年度開始日"""

    business_year_end_date: str = field(default="", metadata={"key": "事業年度終了日"})
    """事業年度終了日"""

    individual_specified_by_law_validity_start_date: str = field(
        default="", metadata={"key": "条例個別指定：有効期間(開始日)"}
    )
    """条例個別指定：有効期間(開始日)"""

    individual_specified_by_law_validity_expiration_date: str = field(
        default="", metadata={"key": "条例個別指定：有効期間(満了日)"}
    )
    """条例個別指定：有効期間(満了日)"""

    individual_specified_by_law_validity_update_application_date: str = field(
        default="", metadata={"key": "条例個別指定：有効期限（更新申請日)"}
    )
    """条例個別指定：有効期限（更新申請日)"""

    individual_specified_by_law_validity_update_date: str = field(
        default="", metadata={"key": "条例個別指定：有効期限（更新日)"}
    )
    """条例個別指定：有効期限（更新日)"""

    individual_specified_by_law_validity_cancellation_date: str = field(
        default="", metadata={"key": "条例個別指定：有効期限（条例個別指定：取消日)"}
    )
    """条例個別指定：有効期限（条例個別指定：取消日)"""


@dataclass(frozen=True)
class OutputApprovedNpoRow(CsvRow):
    """
    出力するための認定NPO法人のデータ

    ※現在はApprovedNpoRow, AllNpoDataRowを結合したデータを出力しているが、将来的には項目を精査する
    """

    # ApprovedNpoRowのフィールド
    approved_npo_control_code: str = field(default="", metadata={"key": "所轄庁コード"})
    """所轄庁コード"""

    approved_npo_control_office: str = field(default="", metadata={"key": "所轄庁"})
    """所轄庁"""

    approved_npo_corporate_number: str = field(default="", metadata={"key": "法人番号"})
    """法人番号"""

    approved_npo_approved: str = field(default="", metadata={"key": "認定"})
    """認定"""

    approved_npo_special_approved: str = field(default="", metadata={"key": "特例認定"})
    """特例認定"""

    approved_npo_update_application: str = field(default="", metadata={"key": "更新申請中"})
    """更新申請中"""

    approved_npo_corporation_name: str = field(default="", metadata={"key": "法人名"})
    """法人名"""

    approved_npo_head_office_address: str = field(
        default="", metadata={"key": "主たる事務所の所在地"}
    )
    """主たる事務所の所在地"""

    approved_npo_representative_name: str = field(default="", metadata={"key": "代表者氏名"})
    """代表者氏名"""

    approved_npo_pst_relative_value: str = field(default="", metadata={"key": "PST基準 相対値"})
    """PST基準 相対値"""

    approved_npo_pst_absolute_value: str = field(default="", metadata={"key": "PST基準 絶対値"})
    """PST基準 絶対値"""

    approved_npo_pst_specified_by_law: str = field(default="", metadata={"key": "PST基準 条例指定"})
    """PST基準 条例指定"""

    approved_npo_pst_specified_by_law_local_government_name: str = field(
        default="", metadata={"key": "PST基準 条例指定 自治体名"}
    )
    """PST基準 条例指定 自治体名"""

    approved_npo_approved_validity_period_from: str = field(
        default="", metadata={"key": "認定有効期間 自"}
    )
    """認定有効期間 自"""

    approved_npo_approved_validity_period_to: str = field(
        default="", metadata={"key": "認定有効期間 至"}
    )
    """認定有効期間 至"""

    approved_npo_special_approved_validity_period_from: str = field(
        default="", metadata={"key": "特例認定有効期間 自"}
    )
    """特例認定有効期間 自"""

    approved_npo_special_approved_validity_period_to: str = field(
        default="", metadata={"key": "特例認定有効期間 至"}
    )
    """特例認定有効期間 至"""

    # AllNpoDataRowのフィールド
    all_npo_corporation_name: str = field(default="", metadata={"key": "法人名称"})
    """法人名称"""

    all_npo_corporation_name_kana: str = field(default="", metadata={"key": "法人名称カナ"})
    """法人名称カナ"""

    all_npo_control_office: str = field(default="", metadata={"key": "所轄庁"})
    """所轄庁"""

    all_npo_delegated_municipality: str = field(default="", metadata={"key": "権限移譲先市町村"})
    """権限移譲先市町村"""

    all_npo_head_office_address: str = field(default="", metadata={"key": "主たる事務所の所在地"})
    """主たる事務所の所在地"""

    all_npo_head_office_postal_code: str = field(
        default="", metadata={"key": "主たる事業所の郵便番号"}
    )
    """主たる事業所の郵便番号"""

    all_npo_branch_office_address: str = field(default="", metadata={"key": "従たる事務所の所在地"})
    """従たる事務所の所在地"""

    all_npo_representative_name: str = field(default="", metadata={"key": "代表者氏名"})
    """代表者氏名"""

    all_npo_representative_name_kana: str = field(
        default="", metadata={"key": "団体代表者名（フリガナ）"}
    )
    """団体代表者名（フリガナ）"""

    all_npo_corporate_establishment_certification_date: str = field(
        default="", metadata={"key": "法人設立認証年月日"}
    )
    """法人設立認証年月日"""

    all_npo_establishment_date: str = field(default="", metadata={"key": "設立年月日"})
    """設立年月日"""

    all_npo_purpose_described_in_the_articles: str = field(
        default="", metadata={"key": "定款に記載された目的"}
    )
    """定款に記載された目的"""

    all_npo_activity_area_1: str = field(default="", metadata={"key": "活動分野１"})
    """活動分野１"""

    all_npo_activity_area_2: str = field(default="", metadata={"key": "活動分野２"})
    """活動分野２"""

    all_npo_activity_area_3: str = field(default="", metadata={"key": "活動分野３"})
    """活動分野３"""

    all_npo_activity_area_4: str = field(default="", metadata={"key": "活動分野４"})
    """活動分野４"""

    all_npo_activity_area_5: str = field(default="", metadata={"key": "活動分野５"})
    """活動分野５"""

    all_npo_activity_area_6: str = field(default="", metadata={"key": "活動分野６"})
    """活動分野６"""

    all_npo_activity_area_7: str = field(default="", metadata={"key": "活動分野７"})
    """活動分野７"""

    all_npo_activity_area_8: str = field(default="", metadata={"key": "活動分野８"})
    """活動分野８"""

    all_npo_activity_area_9: str = field(default="", metadata={"key": "活動分野９"})
    """活動分野９"""

    all_npo_activity_area_10: str = field(default="", metadata={"key": "活動分野１０"})
    """活動分野１０"""

    all_npo_activity_area_11: str = field(default="", metadata={"key": "活動分野１１"})
    """活動分野１１"""

    all_npo_activity_area_12: str = field(default="", metadata={"key": "活動分野１２"})
    """活動分野１２"""

    all_npo_activity_area_13: str = field(default="", metadata={"key": "活動分野１３"})
    """活動分野１３"""

    all_npo_activity_area_14: str = field(default="", metadata={"key": "活動分野１４"})
    """活動分野１４"""

    all_npo_activity_area_15: str = field(default="", metadata={"key": "活動分野１５"})
    """活動分野１５"""

    all_npo_activity_area_16: str = field(default="", metadata={"key": "活動分野１６"})
    """活動分野１６"""

    all_npo_activity_area_17: str = field(default="", metadata={"key": "活動分野１７"})
    """活動分野１７"""

    all_npo_activity_area_18: str = field(default="", metadata={"key": "活動分野１８"})
    """活動分野１８"""

    all_npo_activity_area_19: str = field(default="", metadata={"key": "活動分野１９"})
    """活動分野１９"""

    all_npo_activity_area_20: str = field(default="", metadata={"key": "活動分野２０"})
    """活動分野２０"""

    all_npo_approved_1: str = field(default="", metadata={"key": "認定（認定・特例認定１）"})
    """認定（認定・特例認定１）"""

    all_npo_approved_2: str = field(default="", metadata={"key": "認定（認定・特例認定２）"})
    """認定（認定・特例認定２）"""

    all_npo_approved_3: str = field(default="", metadata={"key": "認定（認定・特例認定３）"})
    """認定（認定・特例認定３）"""

    all_npo_approved_4: str = field(default="", metadata={"key": "認定（認定・特例認定４）"})
    """認定（認定・特例認定４）"""

    all_npo_pst_standard_1: str = field(default="", metadata={"key": "認定（PST基準１）"})
    """認定（PST基準１）"""

    all_npo_pst_standard_2: str = field(default="", metadata={"key": "認定（PST基準２）"})
    """認定（PST基準２）"""

    all_npo_pst_standard_3: str = field(default="", metadata={"key": "認定（PST基準３）"})
    """認定（PST基準３）"""

    all_npo_pst_standard_specified_by_law: str = field(
        default="", metadata={"key": "認定（PST基準 条例指定（都道府県及び市区町村名））"}
    )
    """認定（PST基準 条例指定（都道府県及び市区町村名））"""

    all_npo_approved_start_date: str = field(default="", metadata={"key": "認定（認定開始日）"})
    """認定（認定開始日）"""

    all_npo_approved_expiration_date: str = field(
        default="", metadata={"key": "認定（認定満了日）"}
    )
    """認定（認定満了日）"""

    all_npo_approved_cancellation_date: str = field(
        default="", metadata={"key": "認定（認定取消日）"}
    )
    """認定（認定取消日）"""

    all_npo_special_approved_date: str = field(
        default="", metadata={"key": "認定（特例認定年月日）"}
    )
    """認定（特例認定年月日）"""

    all_npo_special_approved_expiration_date: str = field(
        default="", metadata={"key": "認定（特例認定満了日）"}
    )
    """認定（特例認定満了日）"""

    all_npo_special_approved_cancellation_date: str = field(
        default="", metadata={"key": "認定（特例認定取消日）"}
    )
    """認定（特例認定取消日）"""

    all_npo_supervision_information: str = field(default="", metadata={"key": "監督情報"})
    """監督情報"""

    all_npo_dissolution_information: str = field(default="", metadata={"key": "解散情報"})
    """解散情報"""

    all_npo_corporate_information_url: str = field(default="", metadata={"key": "法人情報URL"})
    """法人情報URL"""

    all_npo_corporate_number: str = field(default="", metadata={"key": "法人番号"})
    """法人番号"""

    all_npo_individual_specified_by_law_flag: str = field(
        default="", metadata={"key": "条例個別指定フラグ"}
    )
    """条例個別指定フラグ"""

    all_npo_specific_non_profit_activities: str = field(
        default="", metadata={"key": "特定非営利活動に係る事業"}
    )
    """特定非営利活動に係る事業"""

    all_npo_other_business: str = field(default="", metadata={"key": "その他の事業"})
    """その他の事業"""

    all_npo_business_year_start_date: str = field(default="", metadata={"key": "事業年度開始日"})
    """事業年度開始日"""

    all_npo_business_year_end_date: str = field(default="", metadata={"key": "事業年度終了日"})
    """事業年度終了日"""

    all_npo_individual_specified_by_law_validity_start_date: str = field(
        default="", metadata={"key": "条例個別指定：有効期間(開始日)"}
    )
    """条例個別指定：有効期間(開始日)"""

    all_npo_individual_specified_by_law_validity_expiration_date: str = field(
        default="", metadata={"key": "条例個別指定：有効期間(満了日)"}
    )
    """条例個別指定：有効期間(満了日)"""

    all_npo_individual_specified_by_law_validity_update_application_date: str = field(
        default="", metadata={"key": "条例個別指定：有効期限（更新申請日)"}
    )
    """条例個別指定：有効期限（更新申請日)"""

    all_npo_individual_specified_by_law_validity_update_date: str = field(
        default="", metadata={"key": "条例個別指定：有効期限（更新日)"}
    )
    """条例個別指定：有効期限（更新日)"""

    all_npo_individual_specified_by_law_validity_cancellation_date: str = field(
        default="", metadata={"key": "条例個別指定：有効期限（条例個別指定：取消日)"}
    )
    """条例個別指定：有効期限（条例個別指定：取消日)"""

    # 詳細ページ基本情報
    information_jurisdiction: str = field(default="", metadata={"key": "所轄庁"})
    """所轄庁"""

    information_delegated_municipality: str = field(
        default="", metadata={"key": "権限移譲先市町村"}
    )
    """権限移譲先市町村"""

    information_corporate_name: str = field(default="", metadata={"key": "法人名称"})
    """法人名称"""

    information_corporate_name_kana: str = field(
        default="", metadata={"key": "法人名称（フリガナ）"}
    )
    """法人名称（フリガナ）"""

    information_main_office_postal_code: str = field(
        default="", metadata={"key": "主たる事業所の郵便番号"}
    )
    """主たる事業所の郵便番号"""

    information_main_office_address: str = field(
        default="", metadata={"key": "主たる事務所の所在地"}
    )
    """主たる事務所の所在地"""

    information_secondary_office_address: str = field(
        default="", metadata={"key": "従たる事務所の所在地"}
    )
    """従たる事務所の所在地"""

    information_representative_name: str = field(default="", metadata={"key": "代表者氏名"})
    """代表者氏名"""

    information_representative_name_kana: str = field(
        default="", metadata={"key": "代表者氏名（フリガナ）"}
    )
    """代表者氏名（フリガナ）"""

    information_establishment_approval_date: str = field(
        default="", metadata={"key": "設立認証年月日"}
    )
    """設立認証年月日"""

    information_establishment_date: str = field(default="", metadata={"key": "設立年月日"})
    """設立年月日"""

    information_articles_of_incorporation_purpose: str = field(
        default="", metadata={"key": "定款に記載された目的"}
    )
    """定款に記載された目的"""

    information_activity_fields: str = field(default="", metadata={"key": "活動分野"})
    """活動分野"""

    information_specified_nonprofit_activities: str = field(
        default="", metadata={"key": "特定非営利活動に係る事業"}
    )
    """特定非営利活動に係る事業"""

    information_other_business: str = field(default="", metadata={"key": "その他の事業"})
    """その他の事業"""

    information_fiscal_year_start: str = field(default="", metadata={"key": "事業年度開始日"})
    """事業年度開始日"""

    information_fiscal_year_end: str = field(default="", metadata={"key": "事業年度終了日"})
    """事業年度終了日"""

    information_corporate_number: str = field(default="", metadata={"key": "法人番号"})
    """法人番号"""

    information_approval_status: str = field(default="", metadata={"key": "認定"})
    """認定"""

    information_jurisdiction_public_site: str = field(
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

    # 詳細ページ 閲覧書類
    document_latest_year: str = field(default="", metadata={"key": "ドキュメント最新年度"})
    document_url: str = field(default="", metadata={"key": "ドキュメントURL"})
