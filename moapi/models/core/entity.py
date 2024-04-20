from pydantic import BaseModel

from moapi.models.core.custom_pydantic_fields import MongoObjectId


class Entity(BaseModel):
    mongo_id: MongoObjectId = None
    id: str = None
