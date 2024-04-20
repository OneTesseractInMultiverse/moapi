import pytest

from moapi.moql.errors import SkipError
from moapi.moql.limit_skip_handler import MoQLSkipHandler


class TestLimitHandler:
    def test_when_skip_parameter_has_no_value(self):
        expected: int = 0
        actual: int = MoQLSkipHandler(skip_parameter="skip=").skip
        assert expected == actual

    def test_when_skip_value_has_valid_value(self):
        expected: int = 100
        actual: int = MoQLSkipHandler(skip_parameter="skip=100").skip
        assert expected == actual

    def test_when_skip_value_has_no_numerical_value(self):
        with pytest.raises(ValueError):
            MoQLSkipHandler(skip_parameter="skip=abc").skip

    def test_when_skip_value_is_negative(self):
        with pytest.raises(SkipError):
            MoQLSkipHandler(skip_parameter="skip=-100").skip
