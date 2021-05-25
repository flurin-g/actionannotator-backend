from typing import Optional, List

from pydantic import BaseModel, Field


class TranscriptSchema(BaseModel):
    speaker: str = Field(...)
    text: List[str] = Field(...)
    actionDetected: bool = Field(...)
    truePositive: bool = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "speaker": "me006",
                "text": ["I", "do", "need", "your", "names"],
                "actionDetected": True,
                "truePositive": False
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


def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}
