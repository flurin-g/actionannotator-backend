from fastapi import APIRouter

from src.data_access.annotation import retrieve_annotation
from src.data_access.transcript import retrieve_transcript
from src.data_access.transcript_annotation import retrieve_transcript_annotation
from src.data_model.all import ResponseModel, ErrorResponseModel

router = APIRouter()


# ToDo: add update and delete endpoints


@router.get("/{id}", response_description="Transcript annotation retrieved")
async def get_transcript_annotation(transcript_annotation_id: str):
    """
    :param transcript_annotation_id:
    :return: the meta-data for the transcript and the annotation and the actual
             text and corresponding annotation data for each utterance
    """
    transcript_annotation = await retrieve_transcript_annotation(transcript_annotation_id)
    transcript = await retrieve_transcript(transcript_annotation["transcriptId"])

    annotation = await retrieve_annotation(transcript_annotation["annotationId"])
    # compile meta-data from combined transcript and transcript_annotation
    transcript_data = {**annotation,
                       "name": transcript["name"],
                       "utterances": [{**data, **meta} for data, meta in
                                      zip(transcript["transcript"], transcript_annotation["utterances"])],
                       }
    if transcript_data:
        return ResponseModel(transcript_data, "Transcript annotation retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "Transcript annotation doesn't exist.")
