from bson import ObjectId

from moapi.mocks.connection.mongo_parameters import (
    MongoDBParametersMock,
)
from moapi.models import Entity
from moapi.odm.connection import MongoDBParameters
from moapi.odm.entity_service import model_to_document

DUMMY_MODEL_ID_FIELD: str = "id"
DUMMY_MODEL_TITLE: str = "Model"
DUMMY_MODEL_TITLE_FIELD: str = "title"
DUMMY_MODEL_TITLE_UPDATED: str = "Updated Title"
DUMMY_MODEL_ID: str = "id_01"
OBJECT_ID_VALUE: str = "6502104e8fb95f068e3a4635"
MONGO_INTERNAL_ID_FILED: str = "_id"
OBJECT_ID_BASE: str = "6509f10e4314386ae084b3c"


class DummyModel(Entity):
    title: str


def get_dummy_model() -> DummyModel:
    return DummyModel(
        title=DUMMY_MODEL_TITLE,
        id=DUMMY_MODEL_ID,
        mongo_id=OBJECT_ID_VALUE,
    )


def get_dummy_model_data() -> dict:
    return model_to_document(get_dummy_model())


def get_connection_parameters() -> MongoDBParameters:
    return MongoDBParametersMock()


def generate_list_of_models(amount: int = 10):
    entities: list[DummyModel] = []
    for index in range(amount):
        model: DummyModel = get_dummy_model()
        model.id = f"{DUMMY_MODEL_ID}-{index}"
        model.title = f"{DUMMY_MODEL_TITLE}-{index}"
        model.mongo_id = ObjectId(f"{OBJECT_ID_BASE}{index}")
        entities.append(model)
    return entities


def generate_list_of_documents(amount: int = 10, remove_ids: bool = False):
    document_list: list[dict] = []
    for model in generate_list_of_models(amount=amount):
        document: dict = model_to_document(model=model)
        if remove_ids and MONGO_INTERNAL_ID_FILED in document:
            document.pop(MONGO_INTERNAL_ID_FILED)
        document_list.append(document)
    return document_list
