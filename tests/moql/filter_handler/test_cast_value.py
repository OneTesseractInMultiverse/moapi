from moapi.moql.filter_handler import MoQLFilter


class TestCastValue:
    def test_with_custom_caster_and_custom_rule(self):
        expected: str = "1.44"
        actual: str = MoQLFilter(
            filter_parameter="string(1.44)", custom_casters={"string": str}
        ).cast_value()
        assert expected == actual

    def test_with_custom_caster_without_custom_rule(self):
        expected: float = 1.44
        actual: str = MoQLFilter(
            filter_parameter="1.44", custom_casters={"string": str}
        ).cast_value()
        assert expected == actual

    def test_without_custom_caster(self):
        expected: float = 1.44
        actual: str = MoQLFilter(
            filter_parameter="1.44", custom_casters=None
        ).cast_value()
        assert expected == actual
