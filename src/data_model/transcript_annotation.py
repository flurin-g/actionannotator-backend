from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field

from src.data_model.mongo_base import MongoModel, PyObjectId


class ActionItemState(str, Enum):
    maybe = "maybe"
    no = "no"
    yes = "yes"


class UtteranceAnnotationIn(BaseModel):
    isActionItem: ActionItemState = Field(...)


class UtteranceAnnotationOut(BaseModel):
    isActionItem: ActionItemState = Field(...)
    text: str = Field(...)
    speaker: str = Field(...)


class TranscriptAnnotationOut(MongoModel):
    annotationId: Optional[PyObjectId]
    transcriptId: Optional[PyObjectId]
    name: Optional[str]
    utterances: Optional[List[UtteranceAnnotationOut]]

    class Config:
        schema_extra = {
            "example": {
                "annotationId": 123456,
                "utterances": [
                    {
                        "isActionItem": "maybe"
                    },
                    {
                        "isActionItem": "yes"
                    }
                ]
            }
        }


class TranscriptAnnotationIn(MongoModel):
    utterances: Optional[List[UtteranceAnnotationIn]]

