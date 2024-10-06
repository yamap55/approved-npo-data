from logging import INFO, getLogger

from approved_npo_data.util.enumerate import controlled_enumerate

logger = getLogger(__name__)


class TestControlledEnumerate:
    class TestBasicFunctionality:
        def test_enumerates_correctly(self):
            data = ["a", "b", "c"]

            expected = [(0, "a"), (1, "b"), (2, "c")]
            acutual = list(controlled_enumerate(data))

            assert acutual == expected

        def test_log_interval(self, caplog):
            data = ["a", "b", "c", "d"]

            with caplog.at_level(INFO):
                list(controlled_enumerate(data, log_interval=2))

            expected = ["1/4", "3/4"]
            acutual = [record.message for record in caplog.records]

            assert acutual == expected

        def test_empty_data(self):
            data = []

            expected = []
            acutual = list(controlled_enumerate(data))

            assert acutual == expected

    class TestMaxItems:
        def test_limited_enumeration(self):
            data = ["a", "b", "c"]

            expected = [(0, "a"), (1, "b")]
            acutual = list(controlled_enumerate(data, max_items=2))

            assert acutual == expected

        def test_max_items_none(self):
            data = ["a", "b", "c"]

            expected = [(0, "a"), (1, "b"), (2, "c")]
            acutual = list(controlled_enumerate(data, max_items=None))

            assert acutual == expected

        def test_max_items_zero(self):
            data = ["a", "b", "c"]

            expected = []
            acutual = list(controlled_enumerate(data, max_items=0))

            assert acutual == expected

        def test_max_items_minus(self):
            data = ["a", "b", "c"]

            expected = []
            acutual = list(controlled_enumerate(data, max_items=-1))

            assert acutual == expected
