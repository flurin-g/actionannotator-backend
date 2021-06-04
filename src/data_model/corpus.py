from typing import Optional, List

from pydantic import BaseModel, Field


class AnnotationSchema(BaseModel):
    name: str = Field(...)
    transcripts: List[dict] = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "name": "My Fancy Annotation",
                "transcripts": [
                    {"name": "Bdb001"},
                    {"name": "Bed002"}
                ]
            }
        }

# ToDo: how to implement the UpdateTranscriptModel, and are additional models needed?
