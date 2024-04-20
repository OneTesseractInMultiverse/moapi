import datetime

from moapi.moql.date_parser import parse_date


class TestParseDate:
    def test_date_conversion(self):
        expected: datetime.datetime = datetime.datetime(
            day=10, month=11, year=2023
        )
        actual: datetime.datetime = parse_date("2023-11-10")
        assert expected == actual

    def test_date_conversion_slashes(self):
        expected: datetime.datetime = datetime.datetime(
            day=10, month=11, year=2023
        )
        actual: datetime.datetime = parse_date("2023/11/10")
        assert expected == actual

    def test_date_conversion_with_time(self):
        expected: datetime.datetime = datetime.datetime(
            day=10, month=11, year=2023, hour=23, minute=30, second=40
        )
        actual: datetime.datetime = parse_date("2023-11-10 23:30:40")
        assert expected == actual

    def test_date_conversion_with_time_with_slashes(self):
        expected: datetime.datetime = datetime.datetime(
            day=10, month=11, year=2023, hour=23, minute=30, second=40
        )
        actual: datetime.datetime = parse_date("2023/11/10 23:30:40")
        assert expected == actual
