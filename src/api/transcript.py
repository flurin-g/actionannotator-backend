from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from src.data_access.transcript import (
    add_transcript,
    delete_transcript,
    retrieve_transcript,
    retrieve_transcripts,
    update_transcript,
)
from src.data_model.transcript_annotation import (
    TranscriptAnnotationSchema,
    UpdateTranscriptModel,
)
from src.data_model.all import ResponseModel, ErrorResponseModel

router = APIRouter()


@router.post("/", response_description="Transcript data added into the database")
async def add_transcript_data(transcript: TranscriptAnnotationSchema = Body(...)):
    transcript = jsonable_encoder(transcript)
    new_transcript = await add_transcript(transcript)
    return ResponseModel(new_transcript, "Transcript added successfully.")


@router.get("/{id}", response_description="Transcripts retrieved")
async def get_transcripts(corpus_id):
    transcript = await retrieve_transcripts(corpus_id)
    if transcript:
        return ResponseModel(transcript, "Transcript data retrieved successfully")
    return ResponseModel(transcript, "Empty list returned")


@router.get("/{id}", response_description="Transcript data retrieved")
async def get_transcript(transcript_id):
    transcript = await retrieve_transcript(transcript_id)
    if transcript:
        return ResponseModel(transcript, "Transcript data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "Transcript doesn't exist.")


@router.put("/{id}")
async def update_transcript_data(transcript_id: str, req: UpdateTranscriptModel = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_transcript = await update_transcript(transcript_id, req)
    if updated_transcript:
        return ResponseModel(
            "Transcript with ID: {} name update is successful".format(transcript_id),
            "Transcript name updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the transcript data.",
    )


@router.delete("/{id}", response_description="Transcript data deleted from the database")
async def delete_transcript_data(transcript_id: str):
    deleted_transcript = await delete_transcript(transcript_id)
    if deleted_transcript:
        return ResponseModel(
            "Transcript with ID: {} removed".format(transcript_id), "Transcript deleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred", 404, "Transcript with id {0} doesn't exist".format(transcript_id)
    )
