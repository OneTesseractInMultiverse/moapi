from moapi.moql.sort_handler import MoQLSortHandler


class TestQueryElement:
    def test_with_single_value_asc(self):
        expected: list[tuple[str, int]] = [("key1", 1)]
        actual: list[tuple[str, int]] = MoQLSortHandler(
            "sort=+key1"
        ).query_element
        assert expected == actual

    def test_with_single_value_desc(self):
        expected: list[tuple[str, int]] = [("key1", -1)]
        actual: list[tuple[str, int]] = MoQLSortHandler(
            "sort=-key1"
        ).query_element
        assert expected == actual

    def test_with_single_value(self):
        expected: list[tuple[str, int]] = [("key1", 1)]
        actual: list[tuple[str, int]] = MoQLSortHandler(
            "sort=key1"
        ).query_element
        assert expected == actual

    def test_with_no_value(self):
        expected: None = None
        actual: list[tuple[str, int]] = MoQLSortHandler("").query_element
        assert expected == actual
