from dataclasses import dataclass, field

from approved_npo_data.util.model_base import ModelBase


@dataclass(frozen=True)
class SampleModel(ModelBase):
    """テスト用のデータモデル"""

    value1: str = field(metadata={"key": "Value1"})
    value2: int = field(metadata={"key": "Value2"})

    id: int = field(default=0, metadata={"key": "ID"})
    name: str = field(default="", metadata={"key": "Name", "optional": True})
    list_value: list[str] = field(default_factory=list, metadata={"key": "ListValue"})


class SampleModelBase:
    """ModelBaseクラスのユニットテストクラス"""

    def test_empty_instance(self):
        """emptyInstance メソッドのテスト"""
        empty_instance = SampleModel.emptyInstance()
        assert empty_instance.value1 == ""
        assert empty_instance.value2 == 0
        assert empty_instance.id == 0
        assert empty_instance.name == ""
        assert empty_instance.list_value == []

    def test_get_field_mapping(self):
        """get_field_mapping メソッドのテスト"""
        expected_mapping = {
            "Value1": "value1",
            "Value2": "value2",
            "ID": "id",
            "Name": "name",
            "ListValue": "list_value",
        }
        assert SampleModel.get_field_mapping() == expected_mapping

    def test_validate_data_keys_warning_for_unknown_key(self, caplog):
        """_validate_data_keysメソッドの未知のキーに対する警告テスト"""
        data = {"Value1": "test", "UnknownKey": "value"}
        with caplog.at_level("WARNING"):
            SampleModel._validate_data_keys(data)
        assert "未知のキーが存在します" in caplog.text

    def test_validate_data_keys_warning_for_missing_key(self, caplog):
        """_validate_data_keysメソッドの欠損キーに対する警告テスト"""
        data = {"Value1": "test"}
        with caplog.at_level("WARNING"):
            SampleModel._validate_data_keys(data)
        assert "必要なキーが存在しませんでした" in caplog.text

    def test_from_dict(self):
        """from_dict メソッドのテスト"""
        instance = SampleModel.from_dict(
            {
                "Value1": "test1",
                "Value2": 100,
                "ID": 1,
                "Name": "test",
                "ListValue": ["item1", "item2"],
            }
        )
        assert instance.value1 == "test1"
        assert instance.value2 == 100
        assert instance.id == 1
        assert instance.name == "test"
        assert instance.list_value == ["item1", "item2"]

    def test_get_csv_header(self):
        """get_csv_header メソッドのテスト"""
        expected_header = ["Value1", "Value2", "ID", "Name", "ListValue"]
        assert SampleModel.get_csv_header() == expected_header

    def test_to_csv_row(self):
        """to_csv_row メソッドのテスト"""
        instance = SampleModel(
            value1="test1", value2=100, id=1, name="test", list_value=["item1", "item2"]
        )
        assert instance.to_csv_row() == ["test1", 100, 1, "test", ["item1", "item2"]]
