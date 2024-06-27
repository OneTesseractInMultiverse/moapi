from typing import TypeVar, Generic, Optional, Iterable, Callable

from pydantic import BaseModel
from pymongo.collection import Collection
from pymongo.results import InsertOneResult, UpdateResult

from moapi.moql.casters import (
    cast_as_list,
    cast_as_timestamp,
    cast_as_object_id,
    cast_as_object_id_ts,
    cast_as_str,
)
from moapi.moql.core import MoQL

from moapi.models.core.entity import Entity
from moapi.odm.connection import (
    MongoDBParameters,
)

MONGO_MODEL_ID_KEY: str = "mongo_id"
MONGO_INTERNAL_ID_KEY: str = "_id"
DEFAULT_HQL_CASTERS: dict[str, Callable] = {
    "list": cast_as_list,
    "object_id": cast_as_object_id,
    "object_id_ts": cast_as_object_id_ts,
    "ts": cast_as_timestamp,
    "str": cast_as_str,
}

MoAPIType = TypeVar("MoAPIType", bound=Entity)
OutputMoAPIType = TypeVar("OutputMoAPIType", bound=BaseModel)


def handle_mongo_internal_id(model_data: dict) -> dict:
    if MONGO_MODEL_ID_KEY in model_data.keys():
        mongo_internal_id = model_data.pop(MONGO_MODEL_ID_KEY)
        model_data[MONGO_INTERNAL_ID_KEY] = mongo_internal_id
    return model_data


def traverse_cursor_and_copy(cursor):
    """
    Helper function that creates a local copy in-memory
    of the results obtained after traversing a cursor
    that is created as a result of a query with high
    projection. This enables data transformations on the
    results without losing the state of the returned
    documents.
    :param cursor: Iterable cursor that points to the
    results from the query.
    :return: A local copy (stored in Heap memory segment)
    of results (List of dictionaries).
    """
    result_set: list = []
    for result in cursor:
        result_set.append(result.copy())
    return result_set


def model_to_document(model: MoAPIType) -> dict:
    """
    Converts an instance of a model to a dictionary that can be stored as a
    MongoDB Document.

    :param model: Instance
    :return: dictionary representation of the model
    """
    model_data: dict = model.model_dump()
    return handle_mongo_internal_id(model_data=model_data)


def document_to_model(
        model_type: type[MoAPIType], document: dict
) -> MoAPIType:
    # Make a local copy in case document is a reference from a cursor
    document_data: dict = document.copy()
    if MONGO_INTERNAL_ID_KEY in document_data:
        document_data[MONGO_MODEL_ID_KEY] = document_data.pop(
            MONGO_INTERNAL_ID_KEY
        )
    return model_type.model_validate(document_data, strict=True)


def document_list_to_model_list(
        model_type: type[MoAPIType], documents: Iterable[dict]
) -> Iterable[MoAPIType]:
    model_list: list = []
    for document in documents:
        model_list.append(
            document_to_model(model_type=model_type, document=document)
        )
    return model_list


def model_list_to_document_list(
        models: Iterable[MoAPIType],
) -> Iterable[dict]:
    document_list: list = []
    for model in models:
        document_list.append(model_to_document(model=model))
    return document_list


class EntityService(Generic[MoAPIType]):
    class Meta:
        collection_name: str

    def __init__(
            self,
            collection_name: str,
            db_connection_parameters: MongoDBParameters,
    ):
        self.collection_name = collection_name
        self.connection_parameters: MongoDBParameters = (
            db_connection_parameters
        )
        self.entities: Collection = self.collection
        self.__document_class = self.get_document_class()

    def get_document_class(self):
        return (
            getattr(self.Meta, "document_class")
            if hasattr(self.Meta, "document_class")
            else self.__orig_bases__[0].__args__[0]  # type: ignore
        )

    @property
    def collection(self) -> Collection:
        return self.connection_parameters.db[self.collection_name]

    def get(
            self,
            query: dict,
            skip: Optional[int] = None,
            limit: Optional[int] = None,
    ):
        """
        Get a list of documents on the given collection based
        on a filter (represented in Python as a dictionary).
        :param limit:
        :param skip:
        :param query: A dictionary containing a valid MongoDB
        filter
        :return: Local copy of results
        """
        # We use deep copy to create local copies that do not
        # reference instances referenced by the cursor and thereby
        # ephemeral
        cursor = self.entities.find(query)
        if skip:
            cursor.skip(skip)
        if limit:
            cursor.limit(limit)
        return traverse_cursor_and_copy(cursor)

    def get_typed(
            self,
            query: dict,
            skip: Optional[int] = None,
            limit: Optional[int] = None,
    ) -> Iterable[MoAPIType]:
        """
        Get a list of documents on a given collection based on a
        mongo query. Documents are returned as instances of models
        instead of plain dictionaries.
        :param limit: sets the maximum amount of results the query
        will return
        :param skip: sets the amount of documents to be skipped
        :param query: Dictionary containing the mongo query
        :return: List of instances of VAPModel derived classes
        """
        return document_list_to_model_list(
            model_type=self.__document_class,
            documents=self.get(query=query, skip=skip, limit=limit),
        )

    def get_one_typed(
            self, identifier_key: str, identifier_value: any
    ) -> Optional[MoAPIType]:
        result = self.entities.find_one({identifier_key: identifier_value})

        return (
            document_to_model(self.__document_class, dict(result))
            if result
            else None
        )

    def add_one_typed(self, model: MoAPIType) -> str:
        """
        Saves entity to database
        :param model: An instance of a class that extends VAPModel
        :return:
        """
        return self.entities.insert_one(
            model_to_document(model)
        ).inserted_id

    def add_one(self, model_data: dict) -> InsertOneResult:
        return self.entities.insert_one(model_data).inserted_id

    def add_many(self, documents: Iterable[dict]):
        return self.entities.insert_many(documents=documents)

    def add_many_typed(self, models: Iterable[MoAPIType]):
        return self.add_many(model_list_to_document_list(models=models))

    def update_one(
            self, filter_data: dict, document: dict
    ) -> UpdateResult:
        return self.entities.update_one(
            filter=filter_data, update={"$set": document}
        )

    def update_one_typed(self, model: MoAPIType) -> UpdateResult:
        values: dict = model_to_document(model=model)
        values.pop(MONGO_INTERNAL_ID_KEY)
        filter_data = {MONGO_INTERNAL_ID_KEY: str(model.mongo_id)}
        return self.update_one(
            filter_data=filter_data,
            document=values,
        )

    def delete_one(self, filter_data: dict):
        return self.entities.delete_one(
            filter=filter_data
        )

    def push_one(
            self,
            match_key: str,
            match_key_value: str,
            match_array: str,
            new_value: any,
    ) -> UpdateResult:
        filter_data: dict = {match_key: match_key_value}
        return self.entities.update_one(
            filter=filter_data, update={"$push": {match_array: new_value}}
        )

    def get_by_moql(self, moql: str) -> list[dict] | None:
        return traverse_cursor_and_copy(
            self.entities.find(
                **MoQL(moql=moql, casters=DEFAULT_HQL_CASTERS).mongo_query
            )
        )
