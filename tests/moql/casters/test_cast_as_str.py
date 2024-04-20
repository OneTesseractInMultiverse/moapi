from moapi.moql.casters import cast_as_str


class TestCastAsStr:
    def test_with_int(self):
        expected: str = "18"
        actual: str = cast_as_str(18)
        assert expected == actual

    def test_with_float(self):
        expected: str = "18.05"
        actual: str = cast_as_str(18.05)
        assert expected == actual
