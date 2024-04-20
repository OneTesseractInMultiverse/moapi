from moapi.moql.filter_handler import find_operator
from moapi.moql.constants import EMPTY_STRING
from tests.moql.core.shared_constants import (
    EQUALS,
    NOT_EQUALS,
    LESS_OR_EQUALS_THAN,
    GREATER_OR_EQUALS_THAN,
    GREATER_THAN,
    LESS_THAN,
    NOT,
)


class TestFindOperator:
    def test_equals_operator(self):
        expected: str = EQUALS
        actual: str = find_operator("key=value")
        assert expected == actual

    def test_not_equals(self):
        expected: str = NOT_EQUALS
        actual: str = find_operator("key!=value")
        assert expected == actual

    def test_less_or_equals_than_operator(self):
        expected: str = LESS_OR_EQUALS_THAN
        actual: str = find_operator("key<=value")
        assert expected == actual

    def test_greater_or_equals_than_operator(self):
        expected: str = GREATER_OR_EQUALS_THAN
        actual: str = find_operator("key>=value")
        assert expected == actual

    def test_greater_than_operator(self):
        expected: str = GREATER_THAN
        actual: str = find_operator("key>value")
        assert expected == actual

    def test_less_than_operator(self):
        expected: str = LESS_THAN
        actual: str = find_operator("key<value")
        assert expected == actual

    def test_exists_operator(self):
        # key
        expected: str = EMPTY_STRING
        actual: str = find_operator("key")
        assert expected == actual

    def test_not_exists_operator(self):
        expected: str = NOT
        actual: str = find_operator("!key")
        assert expected == actual
