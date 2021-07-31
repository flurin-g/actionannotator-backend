from datetime import datetime
from typing import Optional

from bson import ObjectId
from pydantic import BaseConfig, BaseModel, validator


class PyObjectId(ObjectId):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if v and not ObjectId.is_valid(v):
            raise ValueError('Invalid ObjectId')
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type='string')


class MongoModel(BaseModel):
    id: Optional[PyObjectId]

    def __init__(self, **pydict):
        super().__init__(**pydict)
        if "_id" in pydict:
            self.id = pydict.pop('_id')

    class Config(BaseConfig):
        arbitrary_types_allowed = True

        json_encoders = {
            ObjectId: lambda oid: str(oid),
        }

