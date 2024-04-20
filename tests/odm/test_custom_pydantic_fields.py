import pytest
from bson import ObjectId
from moapi.models.core.entity import Entity

MONGO_ID_MOCK_FIELD_NAME: str = "mongo_id"
INVALID_OBJECT_ID: str = "invalid_id"
VALID_OBJECT_ID: str = "711827f2878b88b49ebb69fa"
VAP_ENTITY_ID: str = "72147377-ec77-4ff8-9f7b-af9e5a7dffcf"
VAP_ID_FIELD: str = "id"
EXPECTED_JSON_SCHEMA: dict = {
    "title": "Entity",
    "type": "object",
    "properties": {
        "mongo_id": {
            "default": None,
            "title": "Mongo Id",
            "type": "string",
        },
        "id": {
            "default": None,
            "title": "Id",
            "type": "string",
        },
    },
}


class TestMongoObjectIdField:
    def test_field_validation_raises_value_error_when_invalid_id_provided(
        self,
    ):
        with pytest.raises(ValueError):
            Entity.model_validate(
                {
                    MONGO_ID_MOCK_FIELD_NAME: INVALID_OBJECT_ID,
                    VAP_ID_FIELD: VAP_ENTITY_ID,
                }
            )

    def test_field_validation_passes_when_valid_id_provided(self):
        assert Entity.model_validate(
            {
                MONGO_ID_MOCK_FIELD_NAME: VALID_OBJECT_ID,
                VAP_ID_FIELD: VAP_ENTITY_ID,
            }
        )

    def test_model_serialization(self):
        expected: dict = {
            MONGO_ID_MOCK_FIELD_NAME: VALID_OBJECT_ID,
            VAP_ID_FIELD: VAP_ENTITY_ID,
        }
        actual: dict = Entity(
            mongo_id=ObjectId(VALID_OBJECT_ID), id=VAP_ENTITY_ID
        ).model_dump()
        assert expected == actual

    def test_schema_generation(self):
        expected: dict = EXPECTED_JSON_SCHEMA
        actual: dict = Entity(
            mongo_id=ObjectId(VALID_OBJECT_ID)
        ).model_json_schema()
        assert expected == actual
