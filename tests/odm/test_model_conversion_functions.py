from typing import Iterable

import pytest
from pydantic import ValidationError

from tests.odm.helpers import (
    generate_list_of_models,
    generate_list_of_documents,
)
from moapi.models.core.entity import Entity
from moapi.odm.entity_service import (
    handle_mongo_internal_id,
    model_to_document,
    document_to_model,
    document_list_to_model_list,
    model_list_to_document_list,
)

VALID_OBJECT_ID: str = "711827f2878b88b49ebb69fa"
VAP_DOCUMENT: dict = {
    "_id": VALID_OBJECT_ID,
    "id": "72147377-ec77-4ff8-9f7b-af9e5a7dffcf",
}
VAP_DOCUMENT_INVALID: dict = {"weird_key": "example", "_id": "invalid_id"}
VAP_ENTITY_ID: str = "72147377-ec77-4ff8-9f7b-af9e5a7dffcf"


class TestHandleMongoInternalId:
    def test_mongo_id_is_correctly_converted_in_final_dict(self):
        model: Entity = Entity(mongo_id=VALID_OBJECT_ID, id=VAP_ENTITY_ID)
        expected: dict = VAP_DOCUMENT
        actual: dict = handle_mongo_internal_id(model.model_dump())
        assert expected == actual


class TestModelToDocument:
    def test_mongo_id_is_correctly_converted_when_model_provided(self):
        model: Entity = Entity(mongo_id=VALID_OBJECT_ID, id=VAP_ENTITY_ID)
        expected: dict = VAP_DOCUMENT
        actual: dict = model_to_document(model=model)
        assert expected == actual


class TestDocumentToModel:
    def test_document_is_correctly_converted_to_model_type(self):
        expected: type = Entity
        actual: Entity = document_to_model(
            model_type=Entity, document=VAP_DOCUMENT
        )
        assert isinstance(actual, expected)

    def test_document_to_model_consistency(self):
        expected: Entity = Entity(
            mongo_id=VALID_OBJECT_ID, id=VAP_ENTITY_ID
        )
        actual: Entity = document_to_model(
            model_type=Entity, document=VAP_DOCUMENT
        )
        assert expected.model_dump() == actual.model_dump()

    def test_document_to_model_validation(self):
        with pytest.raises(ValidationError):
            document_to_model(Entity, document=VAP_DOCUMENT_INVALID)


class TestDocumentListToModelList:
    def test_documents_are_correctly_converted(self):
        expected: type = Entity
        actual: Iterable[Entity] = document_list_to_model_list(
            model_type=Entity, documents=generate_list_of_models()
        )
        for doc in actual:
            assert isinstance(doc, expected)


class TestModelListToDocumentList:
    def test_documents_are_correctly_converted(self):
        expected: Iterable[dict] = generate_list_of_documents()
        actual: Iterable[dict] = model_list_to_document_list(
            models=generate_list_of_models()
        )
        assert expected == actual
