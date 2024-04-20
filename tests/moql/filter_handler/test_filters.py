import datetime

import pytest

from moapi.moql.errors import ListOperatorError
from moapi.moql.filter_handler import MoQLFilter


class TestFilters:
    def test_equality_with_custom_caster(self):
        input_param: str = "key=string(34.6)"
        expected: dict = {"key": "34.6"}
        actual: dict = MoQLFilter(input_param, {"string": str}).filter
        assert expected == actual

    def test_equality_for_single_string_value(self):
        input_param: str = "key=value"
        expected: dict = {"key": "value"}
        actual: dict = MoQLFilter(input_param, None).filter
        assert expected == actual

    def test_equality_for_single_int_value(self):
        input_param: str = "key=10"
        expected: dict = {"key": 10}
        actual: dict = MoQLFilter(input_param, None).filter
        assert expected == actual

    def test_equality_for_single_float_value(self):
        input_param: str = "key=10.14"
        expected: dict = {"key": 10.14}
        actual: dict = MoQLFilter(input_param, None).filter
        assert expected == actual

    def test_equality_for_single_date_value(self):
        input_param: str = "key=2023-12-10"
        expected: dict = {
            "key": datetime.datetime(year=2023, day=10, month=12)
        }
        actual: dict = MoQLFilter(input_param, None).filter
        assert expected == actual

    def test_in_operator_for_list_of_strings(self):
        input_param: str = "key=crc,usd"
        expected: dict = {"key": {"$in": ["crc", "usd"]}}
        actual: dict = MoQLFilter(input_param, None).filter
        assert expected == actual

    def test_nin_operator_for_list_of_strings(self):
        input_param: str = "key!=crc,usd"
        expected: dict = {"key": {"$nin": ["crc", "usd"]}}
        actual: dict = MoQLFilter(input_param, None).filter
        assert expected == actual

    def test_exists_operator(self):
        input_param: str = "key"
        expected: dict = {"key": {"$exists": True}}
        actual: dict = MoQLFilter(input_param, None).filter
        assert expected == actual

    def test_not_exists_operator(self):
        input_param: str = "!key"
        expected: dict = {"key": {"$exists": False}}
        actual: dict = MoQLFilter(input_param, None).filter
        assert expected == actual

    def test_gt_operator_with_number(self):
        input_param: str = "key>10"
        expected: dict = {"key": {"$gt": 10}}
        actual: dict = MoQLFilter(input_param, None).filter
        assert expected == actual

    def test_gte_operator_with_number(self):
        input_param: str = "key>=10"
        expected: dict = {"key": {"$gte": 10}}
        actual: dict = MoQLFilter(input_param, None).filter
        assert expected == actual

    def test_lt_operator_with_number(self):
        input_param: str = "key<10"
        expected: dict = {"key": {"$lt": 10}}
        actual: dict = MoQLFilter(input_param, None).filter
        assert expected == actual

    def test_lte_operator_with_number(self):
        input_param: str = "key<=10"
        expected: dict = {"key": {"$lte": 10}}
        actual: dict = MoQLFilter(input_param, None).filter
        assert expected == actual

    def test_not_equals_operator_with_number(self):
        input_param: str = "key!=10"
        expected: dict = {"key": {"$ne": 10}}
        actual: dict = MoQLFilter(input_param, None).filter
        assert expected == actual

    def test_gt_operator_with_float(self):
        input_param: str = "key>10.15"
        expected: dict = {"key": {"$gt": 10.15}}
        actual: dict = MoQLFilter(input_param, None).filter
        assert expected == actual

    def test_gte_operator_with_float(self):
        input_param: str = "key>=10.15"
        expected: dict = {"key": {"$gte": 10.15}}
        actual: dict = MoQLFilter(input_param, None).filter
        assert expected == actual

    def test_lt_operator_with_float(self):
        input_param: str = "key<10.15"
        expected: dict = {"key": {"$lt": 10.15}}
        actual: dict = MoQLFilter(input_param, None).filter
        assert expected == actual

    def test_lte_operator_with_float(self):
        input_param: str = "key<=10.15"
        expected: dict = {"key": {"$lte": 10.15}}
        actual: dict = MoQLFilter(input_param, None).filter
        assert expected == actual

    def test_not_equals_operator_with_float(self):
        input_param: str = "key!=10.15"
        expected: dict = {"key": {"$ne": 10.15}}
        actual: dict = MoQLFilter(input_param, None).filter
        assert expected == actual

    def test_gt_operator_with_date(self):
        input_param: str = "key>2023-01-12"
        expected: dict = {
            "key": {"$gt": datetime.datetime(year=2023, month=1, day=12)}
        }
        actual: dict = MoQLFilter(input_param, None).filter
        assert expected == actual

    def test_gte_operator_with_date(self):
        input_param: str = "key>=2023-01-12"
        expected: dict = {
            "key": {"$gte": datetime.datetime(year=2023, month=1, day=12)}
        }
        actual: dict = MoQLFilter(input_param, None).filter
        assert expected == actual

    def test_lt_operator_with_date(self):
        input_param: str = "key<2023-01-12"
        expected: dict = {
            "key": {"$lt": datetime.datetime(year=2023, month=1, day=12)}
        }
        actual: dict = MoQLFilter(input_param, None).filter
        assert expected == actual

    def test_lte_operator_with_date(self):
        input_param: str = "key<=2023-01-12"
        expected: dict = {
            "key": {"$lte": datetime.datetime(year=2023, month=1, day=12)}
        }
        actual: dict = MoQLFilter(input_param, None).filter
        assert expected == actual

    def test_not_equals_operator_with_date(self):
        input_param: str = "key!=2023-01-12"
        expected: dict = {
            "key": {"$ne": datetime.datetime(year=2023, month=1, day=12)}
        }
        actual: dict = MoQLFilter(input_param, None).filter
        assert expected == actual

    def test_when_invalid_list_operator(self):
        with pytest.raises(ListOperatorError):
            MoQLFilter("key!uds,crc", None).filter()
