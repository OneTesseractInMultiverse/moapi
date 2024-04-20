from moapi.moql.constants import EMPTY_STRING
from moapi.moql.filter_handler import (
    MoQLFilter,
)


class TestExtractKeyValue:
    def test_key_extraction(self):
        expected: str = "key1"
        actual: str = MoQLFilter(
            filter_parameter="key1>1", custom_casters=None
        ).key
        assert expected == actual

    def test_key_extraction_when_no_key(self):
        expected: str = EMPTY_STRING
        actual: str = MoQLFilter(
            filter_parameter="value", custom_casters=None
        ).key
        assert expected == actual

    def test_value_extraction(self):
        expected: str = "1"
        actual: str = MoQLFilter(
            filter_parameter="key1>1", custom_casters=None
        ).value
        assert expected == actual

    def test_operator_extraction(self):
        expected: str = ">"
        actual: str = MoQLFilter(
            filter_parameter="key1>1", custom_casters=None
        ).operator
        assert expected == actual
