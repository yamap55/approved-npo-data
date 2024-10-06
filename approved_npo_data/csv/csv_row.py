"""CSVの行データを表すクラス群"""

from abc import ABC
from dataclasses import dataclass, fields
from typing import Self


@dataclass
class CsvRow(ABC):  # noqa: B024
    """CSVの行データを表す抽象クラス"""

    @classmethod
    def getHeader(cls) -> list[str]:
        """CSVのヘッダを返す"""
        return [f.name for f in fields(cls)]

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


@dataclass
class ApprovedNpoRow(CsvRow):
    """認定NPO法人のデータ"""

    control_code: str
    control_office: str
    corporate_number: str
    approved: str
    special_approved: str
    update_application: str
    corporation_name: str
    head_office_address: str
    representative_name: str
    pst_relative_value: str
    pst_absolute_value: str
    pst_specified_by_law: str
    pst_specified_by_law_local_government_name: str
    approved_validity_period_from: str
    approved_validity_period_to: str
    special_approved_validity_period_from: str
    special_approved_validity_period_to: str

    @classmethod
    def getHeader(cls) -> list[str]:
        """CSVのヘッダを返す"""
        return [
            "所轄庁コード",
            "所轄庁",
            "法人番号",
            "認定",
            "特例認定",
            "更新申請中",
            "法人名",
            "主たる事務所の所在地",
            "代表者氏名",
            "PST基準 相対値",
            "PST基準 絶対値",
            "PST基準 条例指定",
            "PST基準 条例指定 自治体名",
            "認定有効期間 自",
            "認定有効期間 至",
            "特例認定有効期間 自",
            "特例認定有効期間 至",
        ]


@dataclass
class AllNpoDataRow(CsvRow):
    """全NPO法人のデータ"""

    corporation_name: str
    corporation_name_kana: str
    control_office: str
    delegated_municipality: str
    head_office_address: str
    head_office_postal_code: str
    branch_office_address: str
    representative_name: str
    representative_name_kana: str
    corporate_establishment_certification_date: str
    establishment_date: str
    purpose_described_in_the_articles: str
    activity_area_1: str
    activity_area_2: str
    activity_area_3: str
    activity_area_4: str
    activity_area_5: str
    activity_area_6: str
    activity_area_7: str
    activity_area_8: str
    activity_area_9: str
    activity_area_10: str
    activity_area_11: str
    activity_area_12: str
    activity_area_13: str
    activity_area_14: str
    activity_area_15: str
    activity_area_16: str
    activity_area_17: str
    activity_area_18: str
    activity_area_19: str
    activity_area_20: str
    approved_1: str
    approved_2: str
    approved_3: str
    approved_4: str
    pst_standard_1: str
    pst_standard_2: str
    pst_standard_3: str
    pst_standard_specified_by_law: str
    approved_start_date: str
    approved_expiration_date: str
    approved_cancellation_date: str
    special_approved_date: str
    special_approved_expiration_date: str
    special_approved_cancellation_date: str
    supervision_information: str
    dissolution_information: str
    corporate_information_url: str
    corporate_number: str
    individual_specified_by_law_flag: str
    specific_non_profit_activities: str
    other_business: str
    business_year_start_date: str
    business_year_end_date: str
    individual_specified_by_law_validity_start_date: str
    individual_specified_by_law_validity_expiration_date: str
    individual_specified_by_law_validity_update_application_date: str
    individual_specified_by_law_validity_update_date: str
    individual_specified_by_law_validity_cancellation_date: str

    @classmethod
    def getHeader(cls) -> list[str]:
        """CSVのヘッダを返す"""
        return [
            "法人名称",
            "法人名称カナ",
            "所轄庁",
            "権限移譲先市町村",
            "主たる事務所の所在地",
            "主たる事業所の郵便番号",
            "従たる事務所の所在地",
            "代表者氏名",
            "団体代表者名（フリガナ）",
            "法人設立認証年月日",
            "設立年月日",
            "定款に記載された目的",
            "活動分野１",
            "活動分野２",
            "活動分野３",
            "活動分野４",
            "活動分野５",
            "活動分野６",
            "活動分野７",
            "活動分野８",
            "活動分野９",
            "活動分野１０",
            "活動分野１１",
            "活動分野１２",
            "活動分野１３",
            "活動分野１４",
            "活動分野１５",
            "活動分野１６",
            "活動分野１７",
            "活動分野１８",
            "活動分野１９",
            "活動分野２０",
            "認定（認定・特例認定１）",
            "認定（認定・特例認定２）",
            "認定（認定・特例認定３）",
            "認定（認定・特例認定４）",
            "認定（PST基準１）",
            "認定（PST基準２）",
            "認定（PST基準３）",
            "認定（PST基準 条例指定（都道府県及び市区町村名））",
            "認定（認定開始日）",
            "認定（認定満了日）",
            "認定（認定取消日）",
            "認定（特例認定年月日）",
            "認定（特例認定満了日）",
            "認定（特例認定取消日）",
            "監督情報",
            "解散情報",
            "法人情報URL",
            "法人番号",
            "条例個別指定フラグ",
            "特定非営利活動に係る事業",
            "その他の事業",
            "事業年度開始日",
            "事業年度終了日",
            "条例個別指定：有効期間(開始日)",
            "条例個別指定：有効期間(満了日)",
            "条例個別指定：有効期限（更新申請日)",
            "条例個別指定：有効期限（更新日)",
            "条例個別指定：有効期限（条例個別指定：取消日)",
        ]


@dataclass
class OutputApprovedNpoRow(CsvRow):
    """
    出力するための認定NPO法人のデータ

    ※現在はApprovedNpoRow, AllNpoDataRowを結合したデータを出力しているが、将来的には項目を精査する
    """

    # ApprovedNpoRowのフィールド
    approved_npo_data_control_code: str
    approved_npo_data_control_office: str
    approved_npo_data_corporate_number: str
    approved_npo_data_approved: str
    approved_npo_data_special_approved: str
    approved_npo_data_update_application: str
    approved_npo_data_corporation_name: str
    approved_npo_data_head_office_address: str
    approved_npo_data_representative_name: str
    approved_npo_data_pst_relative_value: str
    approved_npo_data_pst_absolute_value: str
    approved_npo_data_pst_specified_by_law: str
    approved_npo_data_pst_specified_by_law_local_government_name: str
    approved_npo_data_approved_validity_period_from: str
    approved_npo_data_approved_validity_period_to: str
    approved_npo_data_special_approved_validity_period_from: str
    approved_npo_data_special_approved_validity_period_to: str

    # AllNpoDataRowのフィールド
    all_npo_data_corporation_name: str
    all_npo_data_corporation_name_kana: str
    all_npo_data_control_office: str
    all_npo_data_delegated_municipality: str
    all_npo_data_head_office_address: str
    all_npo_data_head_office_postal_code: str
    all_npo_data_branch_office_address: str
    all_npo_data_representative_name: str
    all_npo_data_representative_name_kana: str
    all_npo_data_corporate_establishment_certification_date: str
    all_npo_data_establishment_date: str
    all_npo_data_purpose_described_in_the_articles: str
    all_npo_data_activity_area_1: str
    all_npo_data_activity_area_2: str
    all_npo_data_activity_area_3: str
    all_npo_data_activity_area_4: str
    all_npo_data_activity_area_5: str
    all_npo_data_activity_area_6: str
    all_npo_data_activity_area_7: str
    all_npo_data_activity_area_8: str
    all_npo_data_activity_area_9: str
    all_npo_data_activity_area_10: str
    all_npo_data_activity_area_11: str
    all_npo_data_activity_area_12: str
    all_npo_data_activity_area_13: str
    all_npo_data_activity_area_14: str
    all_npo_data_activity_area_15: str
    all_npo_data_activity_area_16: str
    all_npo_data_activity_area_17: str
    all_npo_data_activity_area_18: str
    all_npo_data_activity_area_19: str
    all_npo_data_activity_area_20: str
    all_npo_data_approved_1: str
    all_npo_data_approved_2: str
    all_npo_data_approved_3: str
    all_npo_data_approved_4: str
    all_npo_data_pst_standard_1: str
    all_npo_data_pst_standard_2: str
    all_npo_data_pst_standard_3: str
    all_npo_data_pst_standard_specified_by_law: str
    all_npo_data_approved_start_date: str
    all_npo_data_approved_expiration_date: str
    all_npo_data_approved_cancellation_date: str
    all_npo_data_special_approved_date: str
    all_npo_data_special_approved_expiration_date: str
    all_npo_data_special_approved_cancellation_date: str
    all_npo_data_supervision_information: str
    all_npo_data_dissolution_information: str
    all_npo_data_corporate_information_url: str
    all_npo_data_corporate_number: str
    all_npo_data_individual_specified_by_law_flag: str
    all_npo_data_specific_non_profit_activities: str
    all_npo_data_other_business: str
    all_npo_data_business_year_start_date: str
    all_npo_data_business_year_end_date: str
    all_npo_data_individual_specified_by_law_validity_start_date: str
    all_npo_data_individual_specified_by_law_validity_expiration_date: str
    all_npo_data_individual_specified_by_law_validity_update_application_date: str
    all_npo_data_individual_specified_by_law_validity_update_date: str
    all_npo_data_individual_specified_by_law_validity_cancellation_date: str

    # 詳細ページ情報
    document_latest_year: str
    document_url: str

    @classmethod
    def getHeader(cls) -> list[str]:
        """CSVのヘッダを返す"""
        return (
            ApprovedNpoRow.getHeader()
            + AllNpoDataRow.getHeader()
            + ["ドキュメント最新年度", "ドキュメントURL"]
        )
