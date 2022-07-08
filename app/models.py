from pydantic import BaseModel, Field, PrivateAttr
from pymongo import MongoClient
from bson import ObjectId
from typing import Optional

client = MongoClient()
db = client.test
class PydanticObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not isinstance(v, ObjectId):
            raise TypeError('ObjectId required')
        return str(v)

class User(BaseModel):
    name: str | None = None
    email: str | None = None



class Users(BaseModel):
    id: PydanticObjectId = Field(alias="_id")
    name: str | None = None
    email: str | None = None

    