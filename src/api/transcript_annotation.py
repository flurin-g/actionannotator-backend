from typing import List

from fastapi import APIRouter, Body, HTTPException

from src.api.helper import raise_if_none
from src.data_access.annotation import retrieve_annotation
from src.data_access.transcript import retrieve_transcript
from src.data_access.transcript_annotation import retrieve_transcript_annotation, update_transcript_annotation
from src.data_model.mongo_base import PyObjectId
from src.data_model.transcript_annotation import TranscriptAnnotationOut, UtteranceAnnotationIn, TranscriptAnnotationIn, \
    ActionItemState

router = APIRouter()


@router.get("/{transcript_annotation_id}", response_model=TranscriptAnnotationOut)
async def get_transcript_annotation(transcript_annotation_id: PyObjectId):
    """
    :param transcript_annotation_id:
    :return: the meta-data for the transcript and the annotation and the actual
             text and corresponding annotation data for each utterance
    """
    transcript_data = await fetch_annotated_transcript(transcript_annotation_id)
    return raise_if_none(transcript_data, 404, "Transcript annotation not found")


async def fetch_annotated_transcript(transcript_annotation_id):
    transcript_annotation = await retrieve_transcript_annotation(transcript_annotation_id)
    raise_if_none(transcript_annotation, 404, "Transcript annotation not found")
    transcript = await retrieve_transcript(transcript_annotation["transcriptId"])
    transcript_data = {**dict(transcript_annotation),
                       "name": transcript["name"],
                       "utterances": [{**data, **meta} for data, meta in
                                      zip(transcript["transcript"], transcript_annotation["utterances"])],
                       }
    return transcript_data


@router.put("/{transcript_annotation_id}", response_model=List[UtteranceAnnotationIn])
async def update_utterances_annotation(transcript_annotation_id: PyObjectId, req: TranscriptAnnotationIn = Body(...)):
    await update_transcript_annotation(transcript_annotation_id, req.utterances)
    transcript_annotation = await retrieve_transcript_annotation(transcript_annotation_id)
    return raise_if_none(transcript_annotation["utterances"], 404, "Error updating utterances")


@router.delete("/{transcript_annotation_id}", response_model=List[UtteranceAnnotationIn])
async def delete_utterances_annotation(transcript_annotation_id: PyObjectId):
    transcript_annotation = await retrieve_transcript_annotation(transcript_annotation_id)
    resetted_utterances = [UtteranceAnnotationIn(**{"isActionItem": ActionItemState.maybe}) for _ in
                           transcript_annotation["utterances"]]
    await update_transcript_annotation(transcript_annotation_id, resetted_utterances)
    transcript_annotation = await retrieve_transcript_annotation(transcript_annotation_id)
    return raise_if_none(transcript_annotation["utterances"], 404, "Error resetting utterances")


