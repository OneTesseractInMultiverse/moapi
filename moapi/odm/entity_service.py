from typing import Generic, Optional, Iterable

from pymongo.collection import Collection
from pymongo.results import InsertOneResult, UpdateResult
from moapi.moql.core import MoQL
from moapi.odm.connection import (
    MongoDBParameters,
)
from moapi.odm.types import (
    MONGO_MODEL_ID_KEY,
    MONGO_INTERNAL_ID_KEY,
    DEFAULT_HQL_CASTERS,
    MoAPIType,
)


# =========================================================
# HANDE MONGO INTERNAL ID
# =========================================================
def handle_mongo_internal_id(model_data: dict) -> dict:
    if MONGO_MODEL_ID_KEY in model_data.keys():
        mongo_internal_id = model_data.pop(MONGO_MODEL_ID_KEY)
        model_data[MONGO_INTERNAL_ID_KEY] = mongo_internal_id
    return model_data


# =========================================================
# TRAVERSE CURSOR AND COPY
# =========================================================
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


# =========================================================
# CLASS ENTITY SERVICE
# =========================================================
class EntityService(Generic[MoAPIType]):
    class Meta:
        collection_name: str

    # -----------------------------------------------------
    # CONSTRUCTOR
    # -----------------------------------------------------
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

    # -----------------------------------------------------
    # GET DOCUMENT CLASS
    # -----------------------------------------------------
    def get_document_class(self):
        return (
            getattr(self.Meta, "document_class")
            if hasattr(self.Meta, "document_class")
            else self.__orig_bases__[0].__args__[0]  # type: ignore
        )

    # -----------------------------------------------------
    # PROPERTY COLLECTION
    # -----------------------------------------------------
    @property
    def collection(self) -> Collection:
        return self.connection_parameters.db[self.collection_name]

    # -----------------------------------------------------
    # GET
    # -----------------------------------------------------
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

    # -----------------------------------------------------
    # GET TYPED
    # -----------------------------------------------------
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

    # -----------------------------------------------------
    # GET ONE
    # -----------------------------------------------------
    def get_one(
        self, identifier_key: str, identifier_value: any
    ) -> Optional[MoAPIType]:
        """

        Args:
            identifier_key:
            identifier_value:

        Returns:

        """
        result = self.entities.find_one({identifier_key: identifier_value})
        return result if result else None

    # -----------------------------------------------------
    # GET ONE TYPED
    # -----------------------------------------------------
    def get_one_typed(
        self, identifier_key: str, identifier_value: any
    ) -> Optional[MoAPIType]:
        """

        Args:
            identifier_key:
            identifier_value:

        Returns:

        """
        result = self.entities.find_one({identifier_key: identifier_value})

        return (
            document_to_model(self.__document_class, dict(result))
            if result
            else None
        )

    # -----------------------------------------------------
    # ADD ONE
    # -----------------------------------------------------
    def add_one(self, model_data: dict) -> InsertOneResult:
        """

        Args:
            model_data:

        Returns:

        """
        return self.entities.insert_one(model_data).inserted_id

    # -----------------------------------------------------
    # ADD ONE TYPED
    # -----------------------------------------------------
    def add_one_typed(self, model: MoAPIType) -> str:
        """
        Saves entity to database
        :param model: An instance of a class that extends VAPModel
        :return:
        """
        return self.entities.insert_one(
            model_to_document(model)
        ).inserted_id

    # -----------------------------------------------------
    # ADD MANY
    # -----------------------------------------------------
    def add_many(self, documents: Iterable[dict]):
        """

        Args:
            documents:

        Returns:

        """
        return self.entities.insert_many(documents=documents)

    # -----------------------------------------------------
    # ADD MANY TYPED
    # -----------------------------------------------------
    def add_many_typed(self, models: Iterable[MoAPIType]):
        """

        Args:
            models:

        Returns:

        """
        return self.add_many(model_list_to_document_list(models=models))

    # -----------------------------------------------------
    # UPDATE ONE
    # -----------------------------------------------------
    def update_one(
        self, filter_data: dict, document: dict
    ) -> UpdateResult:
        """

        Args:
            filter_data:
            document:

        Returns:

        """
        return self.entities.update_one(
            filter=filter_data, update={"$set": document}
        )

    # -----------------------------------------------------
    # UPDATE ONE TYPED
    # -----------------------------------------------------
    def update_one_typed(self, model: MoAPIType) -> UpdateResult:
        """

        Args:
            model:

        Returns:

        """
        values: dict = model_to_document(model=model)
        values.pop(MONGO_INTERNAL_ID_KEY)
        filter_data = {MONGO_INTERNAL_ID_KEY: str(model.mongo_id)}
        return self.update_one(
            filter_data=filter_data,
            document=values,
        )

    # -----------------------------------------------------
    # DELETE ONE
    # -----------------------------------------------------
    def delete_one(self, filter_data: dict):
        """
        TODO write tests
        Args:
            filter_data:

        Returns:

        """
        return self.entities.delete_one(filter=filter_data)

    # -----------------------------------------------------
    # DELETE MANY
    # -----------------------------------------------------
    def delete_many(self, filter_data: dict):
        """

        Args:
            filter_data:

        Returns:

        """
        return self.entities.delete_many(filter=filter_data)

    # -----------------------------------------------------
    # PUSH ONE
    # -----------------------------------------------------
    def push_one(
        self,
        match_key: str,
        match_key_value: str,
        match_array: str,
        new_value: any,
    ) -> UpdateResult:
        """

        Args:
            match_key:
            match_key_value:
            match_array:
            new_value:

        Returns:

        """
        filter_data: dict = {match_key: match_key_value}
        return self.entities.update_one(
            filter=filter_data, update={"$push": {match_array: new_value}}
        )

    # -----------------------------------------------------
    # GET BY MOQL
    # -----------------------------------------------------
    def get_by_moql(self, moql: str) -> list[dict] | None:
        """

        Args:
            moql:

        Returns:

        """
        return traverse_cursor_and_copy(
            self.entities.find(
                **MoQL(moql=moql, casters=DEFAULT_HQL_CASTERS).mongo_query
            )
        )


# =========================================================
# MODEL TO DOCUMENT
# =========================================================
def model_to_document(model: MoAPIType) -> dict:
    """
    Converts an instance of a model to a dictionary that can be stored as a
    MongoDB Document.

    :param model: Instance
    :return: dictionary representation of the model
    """
    model_data: dict = model.model_dump()
    return handle_mongo_internal_id(model_data=model_data)


# =========================================================
# DOCUMENT TO MODEL
# =========================================================
def document_to_model(
    model_type: type[MoAPIType], document: dict
) -> MoAPIType:
    """
    Converts an instance of a model to a dictionary
    that can be stored in a MongoDB Document.
    Args:
        model_type:
        document:

    Returns:

    """
    # Make a local copy in case document is a reference from a cursor
    document_data: dict = document.copy()
    if MONGO_INTERNAL_ID_KEY in document_data:
        document_data[MONGO_MODEL_ID_KEY] = document_data.pop(
            MONGO_INTERNAL_ID_KEY
        )
    return model_type.model_validate(document_data, strict=True)


# =========================================================
# DOCUMENT LIST TO MODEL LIST
# =========================================================
def document_list_to_model_list(
    model_type: type[MoAPIType], documents: Iterable[dict]
) -> Iterable[MoAPIType]:
    model_list: list = []
    for document in documents:
        model_list.append(
            document_to_model(model_type=model_type, document=document)
        )
    return model_list


# =========================================================
# MODEL LIST TO DOCUMENT LIST
# =========================================================
def model_list_to_document_list(
    models: Iterable[MoAPIType],
) -> Iterable[dict]:
    document_list: list = []
    for model in models:
        document_list.append(model_to_document(model=model))
    return document_list
