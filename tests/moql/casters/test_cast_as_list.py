from moapi.moql.casters import cast_as_list


class TestCastAsList:
    def test_with_single_value(self):
        expected: list[str] = ["val1"]
        actual: list[str] = cast_as_list("val1")
        assert expected == actual

    def test_with_no_values(self):
        expected: list[str] = []
        actual: list[str] = cast_as_list("")
        assert expected == actual

    def test_with_multiple_values(self):
        expected: list[str] = ["val1", "val2", "val3"]
        actual: list[str] = cast_as_list("val1,val2,val3")
        assert expected == actual
