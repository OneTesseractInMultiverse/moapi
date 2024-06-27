import logging
from typing import TypeVar, Generic

from moapi.models import Entity

_LOGGER = logging.getLogger(__name__)

MoAPIType = TypeVar("MoAPIType", bound=Entity)

PROPERTIES_DICT_KEY: str = "properties"
PROPERTIES_TYPE_DICT_KEY: str = "type"

PROPERTY_NOT_FOUND_ERROR_TEMPLATE: str = (
    "{field} is not a valid property of the target model"
)
PROPERTY_WRONG_TYPE_ERROR_TEMPLATE: str = (
    "The value provided for {field} is instance of an invalid type"
)

TYPE_MAPPING: dict = {
    "string": str,
    "integer": int,
    "number": float,
    "object": object,
}


class QueryError(Exception):
    pass


class QueryString(Generic[MoAPIType]):
    class Meta:
        pass

    # -----------------------------------------------------
    # CLASS CONSTRUCTOR
    # -----------------------------------------------------
    def __init__(self, query_string: dict):
        self.raw_query: dict = query_string
        self.__document_class = self.get_document_class()
        self.schema: dict = self.__document_class.model_json_schema()
        self.verify_properties()
        _LOGGER.debug(f"Using schema: \n {self.schema}")

    # -----------------------------------------------------
    # METHOD GET DOCUMENT CLASS
    # -----------------------------------------------------
    def get_document_class(self):
        return (
            getattr(self.Meta, "document_class")
            if hasattr(self.Meta, "document_class")
            else self.__orig_bases__[0].__args__[0]  # type: ignore
        )

    # -----------------------------------------------------
    # METHOD VERIFY PROPERTIES
    # -----------------------------------------------------
    def verify_properties(self) -> bool:
        for field in self.raw_query:
            self.verify_field_exists_as_property_in_model(field=field)
            self.verify_type(field=field)
        return True

    # -----------------------------------------------------
    # METHOD VERIFY EXISTS AS PROPERTY IN MODEL
    # -----------------------------------------------------
    def verify_field_exists_as_property_in_model(self, field: str):
        if field not in self.schema.get(PROPERTIES_DICT_KEY):
            raise QueryError(
                PROPERTY_NOT_FOUND_ERROR_TEMPLATE.format(field=field)
            )

    # -----------------------------------------------------
    # METHOD VERIFY TYPES
    # -----------------------------------------------------
    def verify_type(self, field: str):
        if isinstance(
            self.raw_query.get(field),
            TYPE_MAPPING.get(
                self.schema.get(PROPERTIES_DICT_KEY)
                .get(field)
                .get(PROPERTIES_TYPE_DICT_KEY)
            ),
        ):
            return
        raise ValueError(
            PROPERTY_WRONG_TYPE_ERROR_TEMPLATE.format(field=field)
        )

    # -----------------------------------------------------
    # METHOD VERIFY TYPES
    # -----------------------------------------------------

    @property
    def as_mongo_query(self) -> dict | None:
        raise NotImplementedError()  # pragma: no cover
