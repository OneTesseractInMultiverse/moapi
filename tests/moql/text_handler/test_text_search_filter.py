import pytest

from moapi.moql.errors import TextOperatorError
from moapi.moql.text_search_handler import MoQLTextSearch


class TestTextSearchFilter:
    def test_with_valid_text_search_parameter(self):
        parameter: str = "$text=this is a full text search"
        expected: dict = {
            "$text": {"$search": "this is a full text search"}
        }
        actual: dict = MoQLTextSearch(parameter).filter
        assert expected == actual

    def test_with_invalid_text_search_parameter(self):
        parameter: str = "$text="
        with pytest.raises(TextOperatorError):
            MoQLTextSearch(parameter).filter
