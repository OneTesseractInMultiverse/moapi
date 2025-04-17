from typing import Callable, TypeVar

from pydantic import BaseModel

from moapi.models import Entity
from moapi.moql.casters import (
    cast_as_list,
    cast_as_object_id,
    cast_as_object_id_ts,
    cast_as_timestamp,
    cast_as_str,
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
