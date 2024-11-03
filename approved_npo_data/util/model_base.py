"""各データモデルの基底クラス"""

from abc import ABC
from dataclasses import MISSING, Field, dataclass, fields
from logging import getLogger
from typing import Any, Self

logger = getLogger(__name__)


@dataclass(frozen=True)
class ModelBase(ABC):  # noqa: B024
    """各データモデルの基底クラス"""

    @classmethod
    def emptyInstance(cls) -> Self:
        """
        空のインスタンスを返す
        """

        # デフォルト値が設定されていない場合に型に応じた初期値を返す
        def get_initial_value(field_: Field):
            if field_.default is not MISSING:
                # デフォルト値が直接設定されている場合
                return field_.default
            elif field_.default_factory is not MISSING:
                # default_factoryが設定されている場合
                return field_.default_factory()
            else:
                # TODO: int, strのみ対応。他の型にも対応する
                if field_.type is int:
                    return 0
                elif field_.type is str:
                    return ""
                else:
                    return None

        # フィールド名と初期値のペアを辞書にし、インスタンス化
        init_values = {field_.name: get_initial_value(field_) for field_ in fields(cls)}
        return cls(**init_values)

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
    def from_dict(cls, data: dict[str, Any]) -> Self:
        """
        辞書からデータを設定して、インスタンスを生成する。

        Args:
            data (Dict[str, str]): キーと値の辞書。

        Returns:
            Self: 抽出したデータを持つオブジェクト。
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
