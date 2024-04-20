import pytest

from moapi.moql.errors import ProjectionError
from moapi.moql.projection_handler import MoQLProjection


def get_projection_with_json():
    return MoQLProjection(
        projection_parameter=(
            'fields={"vulnerabilities":{"$elemMatch":'
            '{"risk_score": {"$gt": 5}}}},created,last_updated'
        )
    ).projection


def get_projection_with_invalid_json():
    return MoQLProjection(
        projection_parameter=(
            "fields={'vulnerabilities': "
            "{'$elemMatch':{'score': {'$gt': "
            "5}}}},created,last_updated"
        )
    ).projection


class TestProjection:
    def test_when_projection_has_no_value(self):
        expected: any = None
        actual: any = MoQLProjection(
            projection_parameter="fields="
        ).projection
        assert expected == actual

    def test_when_projection_has_inclusion_values(self):
        expected: any = {"_id": 1, "score": 1}
        actual: any = MoQLProjection(
            projection_parameter="fields=_id,score"
        ).projection
        assert expected == actual

    def test_when_projection_has_exclusion_values(self):
        expected: any = {"_id": 0, "score": 0}
        actual: any = MoQLProjection(
            projection_parameter="fields=-_id,-score"
        ).projection
        assert expected == actual

    def test_when_json_is_not_valid(self):
        with pytest.raises(ProjectionError):
            get_projection_with_invalid_json()

    def test_when_projection_has_json_value(self):
        expected: any = {
            "vulnerabilities": {"$elemMatch": {"risk_score": {"$gt": 5}}},
            "created": 1,
            "last_updated": 1,
        }
        assert get_projection_with_json() == expected
