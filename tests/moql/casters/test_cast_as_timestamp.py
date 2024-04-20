import datetime

import pytest

from moapi.moql.casters import cast_as_timestamp


class TestCastAsTimeStamp:
    def test_with_valid_timestamp(self):
        expected: datetime.datetime = datetime.datetime.fromtimestamp(
            1545730073
        )
        actual: datetime.datetime = cast_as_timestamp("1545730073")
        assert expected == actual

    def test_with_invalid_timestamp(self):
        with pytest.raises(ValueError):
            cast_as_timestamp("15457ABCDS")
