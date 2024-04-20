import pytest

from moapi.moql.errors import CustomCasterError
from moapi.moql.filter_handler import custom_cast


class TestCustomCast:
    def test_when_custom_caster_and_valid_rule(self):
        expected: str = "1.44"
        actual: str = custom_cast(
            value="string(1.44)", casters={"string": str}
        )
        assert expected == actual

    def test_when_custom_caster_but_no_matching_rule(self):
        expected: any = None
        actual: str = custom_cast(value="1.44", casters={"string": str})
        assert expected == actual

    def test_when_custom_caster_with_invalid_value(self):
        with pytest.raises(CustomCasterError):
            custom_cast(value="int(xyz)", casters={"int": int})
