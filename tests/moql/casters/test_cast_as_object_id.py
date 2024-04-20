import datetime

import pytest
from bson import ObjectId
from bson.errors import InvalidId

from moapi.moql.casters import cast_as_object_id, cast_as_object_id_ts


class TestCastAsObjectId:
    def test_with_valid_object_id(self):
        expected: ObjectId = ObjectId("507f1f77bcf86cd799439011")
        actual: ObjectId = cast_as_object_id("507f1f77bcf86cd799439011")
        assert expected == actual

    def test_with_non_valid_object_id(self):
        with pytest.raises(InvalidId):
            cast_as_object_id("507f1f")


class TestCastAsObjectIdTs:
    def test_with_valid_object_id(self):
        expected: datetime.datetime = ObjectId(
            "507f1f77bcf86cd799439011"
        ).generation_time
        actual: datetime.datetime = cast_as_object_id_ts(
            "507f1f77bcf86cd799439011"
        )
        assert expected == actual

    def test_with_non_valid_object_id(self):
        with pytest.raises(InvalidId):
            cast_as_object_id_ts("507f1f")
