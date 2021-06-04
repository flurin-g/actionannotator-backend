from typing import Optional, List

from bson import ObjectId
from pydantic import BaseModel, Field


class UtteranceAnnotationSchema(BaseModel):
    keywords: List[str] = Field(...)
    isActionItem: str = "unknown"


class TranscriptAnnotationSchema(BaseModel):
    annotationId: str = Field(...)
    utterances: List[UtteranceAnnotationSchema] = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "annotationId": 123456,
                "utterances": [
                    {
                        "keyword": "foo",
                        "isActionItem": "yes"  # check if enums can be used
                    },
                    {
                        "keyword": "",
                        "isActionItem": "unknown"  # or 'yes' / 'no'
                    }
                ]
            }
        }


class UpdateTranscriptModel(BaseModel):
    speaker: Optional[str]
    text: Optional[List[str]]
    actionDetected: Optional[bool]
    truePositive: Optional[bool]

    class Config:
        schema_extra = {
            "example": {
                "speaker": "me006",
                "text": ["I", "do", "need", "your", "names"],
                "actionDetected": True,
                "truePositive": False
            }
        }
