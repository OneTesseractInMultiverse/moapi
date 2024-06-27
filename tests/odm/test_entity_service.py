from typing import Optional, Iterable

from bson import ObjectId
from pymongo.results import InsertOneResult

from tests.odm.helpers import (
    get_connection_parameters,
    DummyModel,
    get_dummy_model_data,
    get_dummy_model,
    DUMMY_MODEL_ID,
    generate_list_of_documents,
    generate_list_of_models,
    DUMMY_MODEL_TITLE_UPDATED,
)
from moapi.models.core.entity import Entity
from moapi.odm.entity_service import (
    EntityService,
    document_list_to_model_list,
)

COLLECTION_NAME: str = "dummies"
OBJECT_ID_VALUE: str = "6502104e8fb95f068e3a4635"
OBJECT_ID: ObjectId = ObjectId(OBJECT_ID_VALUE)
MODEL_ID_KEY: str = "id"


class DummyModelService(EntityService[DummyModel]):
    def __init__(self):
        super().__init__(COLLECTION_NAME, get_connection_parameters())


class TestAddOne:
    def test_adding_single_plain_dictionary_data_as_document_id(self):
        expected: str = OBJECT_ID_VALUE
        actual: InsertOneResult = DummyModelService().add_one(
            model_data=get_dummy_model_data()
        )
        assert expected == actual

    def test_adding_single_plain_dictionary_data_as_document(self):
        service: DummyModelService = DummyModelService()
        expected: dict = get_dummy_model_data()
        service.add_one(model_data=get_dummy_model_data())
        actual = service.get({})[0]
        assert expected == actual


class TestTypedAddOne:
    def test_adding_single_model_id(self):
        expected: str = OBJECT_ID_VALUE
        actual: str = DummyModelService().add_one_typed(get_dummy_model())
        assert expected == actual

    def test_adding_single_model(self):
        service: DummyModelService = DummyModelService()
        expected: dict = get_dummy_model_data()
        service.add_one_typed(get_dummy_model())
        actual = service.get({})[0]
        assert expected == actual


class TestTypedGetOne:
    def test_typed_get_one_has_correct_type_mapping(self):
        service: DummyModelService = DummyModelService()
        service.add_one_typed(get_dummy_model())
        actual = service.get_one_typed(
            identifier_key=MODEL_ID_KEY,
            identifier_value=DUMMY_MODEL_ID,
        )
        assert isinstance(actual, DummyModel)

    def test_typed_get_one(self):
        service: DummyModelService = DummyModelService()
        service.add_one_typed(get_dummy_model())
        actual: Optional[DummyModel] = service.get_one_typed(
            identifier_key=MODEL_ID_KEY,
            identifier_value=DUMMY_MODEL_ID,
        )
        assert isinstance(actual, DummyModel)


class TestAddMany:
    def test_add_many_with_valid_documents(self):
        service: DummyModelService = DummyModelService()
        service.add_many(generate_list_of_documents(remove_ids=True))
        actual: list[dict] = service.get(query={})
        assert len(actual) == 10

    def test_add_many_typed_deserializes_correctly(self):
        service: DummyModelService = DummyModelService()
        service.add_many(generate_list_of_documents(remove_ids=True))
        actual: Iterable[Entity] = document_list_to_model_list(
            model_type=DummyModel, documents=service.get(query={})
        )
        for model in actual:
            assert isinstance(model, DummyModel)


class TestAddManyTyped:
    def test_add_many_typed_with_valid_documents(self):
        service: DummyModelService = DummyModelService()
        service.add_many_typed(generate_list_of_models())
        actual: list[dict] = service.get(query={})
        assert len(actual) == 10

    def test_add_many_typed_deserializes_correctly(self):
        service: DummyModelService = DummyModelService()
        service.add_many_typed(generate_list_of_models())
        actual: Iterable[Entity] = document_list_to_model_list(
            model_type=DummyModel, documents=service.get(query={})
        )
        for model in actual:
            assert isinstance(model, DummyModel)


class TestGetByHql:
    def test_by_hql_with_empty_query(self):
        service: DummyModelService = DummyModelService()
        service.add_many_typed(generate_list_of_models())
        actual: list[dict] = service.get_by_moql(moql="")
        assert len(actual) == 10

    def test_by_hql_with_simple_filter(self):
        service: DummyModelService = DummyModelService()
        service.add_many_typed(generate_list_of_models())
        actual: list[dict] = service.get_by_moql(
            moql="_id=6509f10e4314386ae084b3c1"
        )
        assert len(actual) == 1


class TestGet:
    def test_returns_correct_number_of_docs_based_on_query(self):
        service: DummyModelService = DummyModelService()
        service.add_many_typed(generate_list_of_models())
        actual: list[dict] = service.get(query={})
        assert len(actual) == 10

    def test_returns_correct_number_of_docs_based_on_skip(self):
        service: DummyModelService = DummyModelService()
        service.add_many_typed(generate_list_of_models())
        actual: list[dict] = service.get(query={}, skip=5)
        assert len(actual) == 5

    def test_returns_correct_number_of_docs_based_on_limit(self):
        service: DummyModelService = DummyModelService()
        service.add_many_typed(generate_list_of_models())
        actual: list[dict] = service.get(query={}, limit=5)
        assert len(actual) == 5


class TestTypedGet:
    def test_returns_correct_number_of_docs_based_on_query(self):
        service: DummyModelService = DummyModelService()
        service.add_many_typed(generate_list_of_models())
        actual: list[DummyModel] = list(service.get_typed(query={}))
        assert len(actual) == 10

    def test_returns_correct_number_of_docs_based_on_skip(self):
        service: DummyModelService = DummyModelService()
        service.add_many_typed(generate_list_of_models())
        actual: list[DummyModel] = list(
            service.get_typed(query={}, skip=5)
        )
        assert len(actual) == 5

    def test_returns_correct_number_of_docs_based_on_limit(self):
        service: DummyModelService = DummyModelService()
        service.add_many_typed(generate_list_of_models())
        actual: list[DummyModel] = list(
            service.get_typed(query={}, limit=5)
        )
        assert len(actual) == 5


class TestUpdateOne:
    def test_fields_are_updated_correctly(self):
        expected: str = DUMMY_MODEL_TITLE_UPDATED
        service: DummyModelService = DummyModelService()
        service.add_one_typed(get_dummy_model())
        service.update_one(
            filter_data={"_id": OBJECT_ID_VALUE},
            document={"title": DUMMY_MODEL_TITLE_UPDATED},
        )
        actual: str = service.get({})[0]["title"]
        assert actual == expected

    def test_non_are_updated_if_no_match(self):
        expected: str = DUMMY_MODEL_TITLE_UPDATED
        service: DummyModelService = DummyModelService()
        service.add_one_typed(get_dummy_model())
        service.update_one(
            filter_data={"_id": "id02"},
            document={"title": DUMMY_MODEL_TITLE_UPDATED},
        )
        actual: str = service.get({})[0]["title"]
        assert actual != expected


class TestUpdateOneTyped:
    def test_fields_are_updated_correctly(self):
        expected: str = DUMMY_MODEL_TITLE_UPDATED
        service: DummyModelService = DummyModelService()
        service.add_one_typed(get_dummy_model())
        to_be_updated: DummyModel = service.get_one_typed(
            identifier_key=MODEL_ID_KEY, identifier_value=DUMMY_MODEL_ID
        )
        to_be_updated.title = DUMMY_MODEL_TITLE_UPDATED
        service.update_one_typed(to_be_updated)
        actual: str = service.get({})[0]["title"]
        assert actual == expected


class TestPushOne:
    def test_element_added_correctly(self):
        service: DummyModelService = DummyModelService()
        dummy_data: dict = get_dummy_model_data()
        dummy_data["array"] = []
        new_item = {"id": 1, "test": 4}
        service.add_one(dummy_data)
        service.push_one(
            match_key=MODEL_ID_KEY,
            match_key_value=DUMMY_MODEL_ID,
            match_array="array",
            new_value=new_item,
        )
        updated_data = service.get_by_moql(
            f"{MODEL_ID_KEY}={DUMMY_MODEL_ID}"
        )
        # assert
        response_has_at_least_one = len(updated_data[0]["array"]) == 1
        response_contains_element = updated_data[0]["array"][0] == new_item
        assert response_has_at_least_one and response_contains_element
