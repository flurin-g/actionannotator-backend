from enum import Enum

from pydantic import Field

from src.data_model.mongo_base import MongoModel


class BaseCorpus(str, Enum):
    icsi = "ICSI"
    isl = "ISL"
    ami = "AMI"


class Corpus(MongoModel):
    name: BaseCorpus = Field(...)

    class Config:
        schema_extra = {
            "example":
                {
                    "corpusId": "123456",
                    "name": "ICSI"
                }
        }

