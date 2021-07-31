from datetime import datetime
from typing import Optional, List

from pydantic import Field, BaseModel

from src.data_model.corpus import BaseCorpus
# ToDo: consider using date-time for date field in Annotation Schema
from src.data_model.mongo_base import MongoModel


class Annotation(BaseModel):
    name: str = Field(...)
    baseCorpus: BaseCorpus = Field(...)


class AnnotationIn(Annotation):
    class Config:
        schema_extra = {
            "example": {
                "name": "My Fancy Annotation",
                "baseCorpus": "ICSI"
            }
        }


class AnnotationOut(Annotation, MongoModel):
    date: Optional[datetime] = Field(...)
    transcripts: Optional[List[dict]]

    class Config:
        schema_extra = {
            "example": {
                "name": "My Fancy Annotation",
                "date": "2012-05-23T17:15:02",
                "baseCorpus": "ICSI",
                "transcript": [
                    {

                    }
                ]
            }
        }
