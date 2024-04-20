import datetime

from moapi.moql.filter_handler import default_cast


class TestDefaultCast:
    def test_default_caster_for_string(self):
        expected: str = "value"
        actual: any = default_cast("value")
        assert expected == actual

    def test_default_caster_for_int(self):
        expected: int = 10
        actual: any = default_cast("10")
        assert expected == actual

    def test_default_caster_for_float(self):
        expected: float = 10.45
        actual: any = default_cast("10.45")
        assert expected == actual

    def test_default_caster_for_date_with_dashes(self):
        expected: datetime.datetime = datetime.datetime(
            day=10, month=1, year=2023
        )
        actual: any = default_cast("2023-01-10")
        assert expected == actual

    def test_default_caster_for_datetime_with_dashes(self):
        expected: datetime.datetime = datetime.datetime(
            day=10, month=1, year=2023, hour=23, minute=30, second=20
        )
        actual: any = default_cast("2023-01-10 23:30:20")
        assert expected == actual

    def test_default_caster_for_datetime_with_utc(self):
        expected: datetime.datetime = datetime.datetime(
            year=2016, month=1, day=1, tzinfo=datetime.timezone.utc
        )
        actual: any = default_cast("2016-01-01T00:00:00.000000+00:00")
        assert expected == actual

    def test_default_caster_for_list(self):
        expected: list[str] = ["crc", "usd"]
        actual: any = default_cast("crc,usd")
        assert expected == actual

    def test_default_caster_for_regex(self):
        expected: str = {"$options": "i", "$regex": "@ibm\\.com$"}
        actual: any = default_cast("/@ibm\\.com$/i")
        assert expected == actual

    def test_default_caster_for_boolean_true(self):
        expected: bool = True
        actual: any = default_cast("true")
        assert expected == actual

    def test_default_caster_for_boolean_false(self):
        expected: bool = False
        actual: any = default_cast("false")
        assert expected == actual

    def test_default_caster_for_null(self):
        expected: any = None
        actual: any = default_cast("null")
        assert expected == actual

    def test_default_caster_for_none(self):
        expected: any = None
        actual: any = default_cast("none")
        assert expected == actual
