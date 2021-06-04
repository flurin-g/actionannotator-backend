from typing import Optional, List

from pydantic import BaseModel, Field


class AnnotationSchema(BaseModel):
    name: str = Field(...)
    date: str = Field(...)
    baseCorpus: str = Field(...)
    keywords: List[str] = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "name": "My Fancy Annotation",
                "date": "4.5.2012",
                "baseCorpus": "ICSI",
                "keywords": ['foo', 'bar', 'baz']
            }
        }

# ToDo: how to implement the UpdateTranscriptModel, and are additional models needed?
