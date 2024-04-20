import datetime

import pymongo
import pytest

from moapi.moql.errors import (
    ListOperatorError,
    FilterError,
    LimitError,
    SkipError,
    TextOperatorError,
)
from moapi.moql.core import MoQL


class TestHQLQuery:
    def test_when_empty_query(self):
        expected = {
            "filter": {},
            "sort": None,
            "skip": 0,
            "limit": 0,
            "projection": None,
        }
        actual = MoQL("").mongo_query
        assert expected == actual


class TestHQLProjection:
    def test_simple_projection(self):
        expected: dict = {
            "filter": {},
            "sort": None,
            "skip": 0,
            "limit": 0,
            "projection": {"_id": 1},
        }
        actual = MoQL("fields=_id").mongo_query
        assert expected == actual

    def test_exclusion_projection(self):
        expected: dict = {
            "filter": {},
            "sort": None,
            "skip": 0,
            "limit": 0,
            "projection": {"_id": 0},
        }
        actual = MoQL("fields=-_id").mongo_query
        assert expected == actual

    def test_embedded_projection(self):
        expected: dict = {
            "filter": {},
            "sort": None,
            "skip": 0,
            "limit": 0,
            "projection": {"settings.group": 1},
        }
        actual = MoQL("fields=settings.group").mongo_query
        assert expected == actual

    def test_multiple_field_projection(self):
        expected: dict = {
            "filter": {},
            "sort": None,
            "skip": 0,
            "limit": 0,
            "projection": {"_id": 1, "score": 1, "status": 1},
        }
        actual = MoQL("fields=_id,score,status").mongo_query
        assert expected == actual

    def test_multiple_exclusion_projection(self):
        expected: dict = {
            "filter": {},
            "sort": None,
            "skip": 0,
            "limit": 0,
            "projection": {"_id": 0, "score": 0, "status": 0},
        }
        actual = MoQL("fields=-_id,-score,-status").mongo_query
        assert expected == actual

    def test_complex_projection(self):
        expected: dict = {
            "filter": {},
            "sort": None,
            "skip": 0,
            "limit": 0,
            "projection": {
                "vulnerabilities": {"$elemMatch": {"score": {"$gt": 5}}},
                "last_seen": 1,
                "due_date": 1,
            },
        }
        actual = MoQL(
            (
                'fields={"vulnerabilities": {"$elemMatch":{"score": {"$gt":'
                " 5}}}},last_seen,due_date"
            )
        ).mongo_query
        assert expected == actual


class TestHQLQueryLimit:
    def test_good_limit(self):
        expected: dict = {
            "filter": {},
            "sort": None,
            "skip": 5,
            "limit": 0,
            "projection": None,
        }
        actual = MoQL("skip=5").mongo_query
        assert expected == actual

    def test_empty_limit(self):
        expected: dict = {
            "filter": {},
            "sort": None,
            "skip": 0,
            "limit": 0,
            "projection": None,
        }
        actual = MoQL("skip=").mongo_query
        assert expected == actual

    def test_negative_limit(self):
        with pytest.raises(SkipError):
            MoQL("skip=-5").mongo_query

    def test_non_numeric_limit(self):
        with pytest.raises(ValueError):
            MoQL("skip=bad_skip").mongo_query


class TestHQLQuerySkip:
    def test_good_limit(self):
        expected: dict = {
            "filter": {},
            "sort": None,
            "skip": 0,
            "limit": 5,
            "projection": None,
        }
        actual = MoQL("limit=5").mongo_query
        assert expected == actual

    def test_empty_limit(self):
        expected: dict = {
            "filter": {},
            "sort": None,
            "skip": 0,
            "limit": 0,
            "projection": None,
        }
        actual = MoQL("limit=").mongo_query
        assert expected == actual

    def test_negative_limit(self):
        with pytest.raises(LimitError):
            MoQL("limit=-5").mongo_query

    def test_non_numeric_limit(self):
        with pytest.raises(ValueError):
            MoQL("limit=bad_limit").mongo_query


class TestRangeQueries:
    def test_simple_range_support(self):
        expected: dict = {
            "filter": {"score": {"$gt": 525, "$lt": 600}},
            "sort": None,
            "skip": 0,
            "limit": 0,
            "projection": None,
        }
        actual = MoQL("score>525&score<600").mongo_query
        assert expected == actual

    def test_range_query_with_blacklist(self):
        expected: dict = {
            "filter": {
                "user_id": {"$gt": 525, "$lt": 600},
                "creation_date": {
                    "$gte": datetime.datetime.fromisoformat(
                        "2022-10-29T00:00:00.000000"
                    ),
                    "$lte": datetime.datetime.fromisoformat(
                        "2022-10-30T00:00:00.000000"
                    ),
                },
            },
            "sort": None,
            "skip": 0,
            "limit": 0,
            "projection": None,
        }
        actual: dict = MoQL(
            "user_id>525&user_id<600&creation_date>=2022-10-29T00:00:00.000000"
            "&creation_date<=2022-10-30T00:00:00.000000",
            blacklist=tuple(["latitude", "longitude"]),
        ).mongo_query
        assert expected == actual


class TestHQLSort:
    def test_empty_sort(self):
        expected = {
            "filter": {},
            "sort": None,
            "skip": 0,
            "limit": 0,
            "projection": None,
        }
        actual = MoQL("sort=").mongo_query
        assert expected == actual

    def test_ascending_sort(self):
        expected = {
            "filter": {},
            "sort": [("_id", pymongo.ASCENDING)],
            "skip": 0,
            "limit": 0,
            "projection": None,
        }
        actual = MoQL("sort=_id").mongo_query
        assert expected == actual

    def test_ascending_sort_with_operator(self):
        expected = {
            "filter": {},
            "sort": [("_id", pymongo.ASCENDING)],
            "skip": 0,
            "limit": 0,
            "projection": None,
        }
        actual = MoQL("sort=+_id").mongo_query
        assert expected == actual

    def test_descending_sort_with_operator(self):
        expected = {
            "filter": {},
            "sort": [("_id", pymongo.DESCENDING)],
            "skip": 0,
            "limit": 0,
            "projection": None,
        }
        actual = MoQL("sort=-_id").mongo_query
        assert expected == actual

    def test_multiple_ascending_sort(self):
        expected = {
            "filter": {},
            "sort": [
                ("_id", pymongo.ASCENDING),
                ("created_at", pymongo.ASCENDING),
                ("price", pymongo.ASCENDING),
            ],
            "skip": 0,
            "limit": 0,
            "projection": None,
        }
        actual = MoQL("sort=_id,created_at,price").mongo_query
        assert expected == actual

    def test_multiple_descending_sort(self):
        expected = {
            "filter": {},
            "sort": [
                ("_id", pymongo.DESCENDING),
                ("created_at", pymongo.DESCENDING),
                ("price", pymongo.DESCENDING),
            ],
            "skip": 0,
            "limit": 0,
            "projection": None,
        }
        actual = MoQL("sort=-_id,-created_at,-price").mongo_query
        assert expected == actual

    def test_multiple_mixed_sort(self):
        expected = {
            "filter": {},
            "sort": [
                ("_id", pymongo.ASCENDING),
                ("created_at", pymongo.DESCENDING),
                ("price", pymongo.ASCENDING),
                ("active", pymongo.DESCENDING),
            ],
            "skip": 0,
            "limit": 0,
            "projection": None,
        }
        actual = MoQL("sort=_id,-created_at,price,-active").mongo_query
        assert expected == actual


class TestHQLFullTextSearch:
    def test_good_text_operator(self):
        expected = {
            "filter": {"$text": {"$search": "full text search"}},
            "sort": None,
            "skip": 0,
            "limit": 0,
            "projection": None,
        }
        actual = MoQL("$text=full text search").mongo_query
        assert expected == actual

    def test_empty_text_operator(self):
        with pytest.raises(TextOperatorError):
            MoQL("$text=").mongo_query


class TestHQLQueryErrors:
    def test_list_operator_error(self):
        with pytest.raises(ListOperatorError):
            MoQL("tags<=CR,US,FR").mongo_query

    def test_filter_error(self):
        with pytest.raises(FilterError):
            MoQL("tags==CR").mongo_query
