from typing import Any

from bson import ObjectId
from pydantic_core import core_schema
from pydantic_core.core_schema import ChainSchema


class MongoObjectId(str):
    """
    Custom field that handles properly BSON's ObjectId type within a
    Pydantic schema
    """

    @classmethod
    def __get_pydantic_core_schema__(
        cls, _source_type: Any, _handler: Any
    ) -> core_schema.CoreSchema:
        object_id_schema: ChainSchema = core_schema.chain_schema(
            [
                core_schema.str_schema(),
                core_schema.no_info_plain_validator_function(cls.validate),
            ]
        )
        return core_schema.json_or_python_schema(
            json_schema=object_id_schema,
            python_schema=core_schema.union_schema(
                [
                    core_schema.is_instance_schema(ObjectId),
                    object_id_schema,
                ]
            ),
            serialization=core_schema.plain_serializer_function_ser_schema(
                lambda x: str(
                    x
                )  # When serializing ObjectId we simply convert it to string
            ),
        )

    @classmethod
    def validate(cls, value):
        if ObjectId.is_valid(value):
            return ObjectId(value)
        raise ValueError("The mongo_id is not a valid ObjectId")
