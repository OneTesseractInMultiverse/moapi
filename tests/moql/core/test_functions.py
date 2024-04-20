from tests.moql.core.shared_constants import (
    INPUT_HQL_URL_ENCODED,
    INPUT_HQL_NOT_ENCODED,
    EXPECTED_PARAMETER_LIST,
    BLACKLIST,
    EXPECTED_PARAMETER_LIST_WITH_BLACKLISTED,
)
from moapi.moql.core import (
    extract_parameter_list,
    remove_blacklisted,
)


class TestRemoveBlacklisted:
    def test_without_blacklist(self):
        expected: list[str] = EXPECTED_PARAMETER_LIST
        actual: list[str] = remove_blacklisted(
            hql_query=INPUT_HQL_URL_ENCODED, blacklist=None
        )
        assert expected == actual

    def test_with_blacklist(self):
        expected: list[str] = EXPECTED_PARAMETER_LIST_WITH_BLACKLISTED
        actual: list[str] = remove_blacklisted(
            hql_query=INPUT_HQL_URL_ENCODED, blacklist=BLACKLIST
        )
        assert expected == actual


class TestExtractParameterList:
    def test_with_url_encoded_hql(self):
        expected: list[str] = EXPECTED_PARAMETER_LIST
        actual: list[str] = extract_parameter_list(
            hql_query=INPUT_HQL_URL_ENCODED
        )
        assert expected == actual

    def test_without_url_encoded_hql(self):
        expected: list[str] = EXPECTED_PARAMETER_LIST
        actual: list[str] = extract_parameter_list(
            hql_query=INPUT_HQL_NOT_ENCODED
        )
        assert expected == actual
