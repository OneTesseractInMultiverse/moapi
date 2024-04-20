import datetime

import pytest

from moapi.adapters.query_string import QueryString, QueryError
from moapi.models import Entity


class DummyModel(Entity):
    severity: str = None
    score: int = 0
    cvss: float = 1.3
    created: datetime.datetime = datetime.datetime.now(datetime.UTC)


class DummyModelQuery(QueryString[DummyModel]):
    def __init__(self, query_string: dict):
        super().__init__(query_string)


SEVERITY_FIELD_NAME: str = "severity"
SEVERITY_FIELD_VALUE: str = "High"
INVALID_FIELD_NAME: str = "invalid_field"
INVALID_FIELD_VALUE: str = "invalid_field_value"
NON_STRING_VALUE: int = 0

CASE_1_SINGLE_PROPERTY_EXACT_MATCH: dict = {
    SEVERITY_FIELD_NAME: SEVERITY_FIELD_VALUE
}
CASE_1_EXPECTED_RESULT: dict = {SEVERITY_FIELD_NAME: SEVERITY_FIELD_VALUE}
INVALID_FIELD_QUERY: dict = {INVALID_FIELD_NAME: INVALID_FIELD_VALUE}
INVALID_VALUE_QUERY: dict = {SEVERITY_FIELD_NAME: NON_STRING_VALUE}
VALID_QUERY: dict = {SEVERITY_FIELD_NAME: SEVERITY_FIELD_VALUE}


class TestSingleFieldExactMatchQuery:
    def test_when_field_not_present_in_schema_error_is_raised(self):
        with pytest.raises(QueryError):
            DummyModelQuery(query_string=INVALID_FIELD_QUERY)

    def test_when_field_value_has_wrong_type_value_error_is_raised(self):
        with pytest.raises(ValueError):
            DummyModelQuery(query_string=INVALID_VALUE_QUERY)

    def test_when_valid_field_and_type_provided_validation_is_true(self):
        assert DummyModelQuery(
            query_string=VALID_QUERY
        ).verify_properties()
