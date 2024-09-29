from approved_npo_data.util.date_format import simple_format_time


class TestSimpleFormatTime:
    class TestInteger:
        def test_zero_seconds(self):
            assert simple_format_time(0) == "0時間0分0秒"

        def test_under_one_minute(self):
            assert simple_format_time(30) == "0時間0分30秒"

        def test_one_minute(self):
            assert simple_format_time(60) == "0時間1分0秒"

        def test_over_one_minute(self):
            assert simple_format_time(90) == "0時間1分30秒"

        def test_one_hour(self):
            assert simple_format_time(3600) == "1時間0分0秒"

        def test_over_one_hour(self):
            assert simple_format_time(3660) == "1時間1分0秒"

        def test_multiple_hours_minutes_seconds(self):
            assert simple_format_time(5432) == "1時間30分32秒"

        def test_large_number_of_seconds(self):
            assert simple_format_time(86399) == "23時間59分59秒"

    class TestFloat:
        def test_float_seconds(self):
            assert simple_format_time(3660.5) == "1時間1分0秒"

        def test_float_seconds_rounding(self):
            assert simple_format_time(3660.9) == "1時間1分0秒"
