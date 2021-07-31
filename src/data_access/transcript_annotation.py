from functools import partial
from typing import List

from bson import ObjectId
from fastapi.encoders import jsonable_encoder

from src.data_access.mongo_connection import transcript_annotation_collection
from src.data_access.transcript import retrieve_transcripts
from src.data_model.annotation import AnnotationOut
from src.data_model.mongo_base import PyObjectId
from src.data_model.transcript_annotation import UtteranceAnnotationIn, ActionItemState


def convert_transcript_to_annotation(annotation_id: PyObjectId, transcript_data: dict) -> dict:
    """
    This function injects the nlp-processing into the data-persistence step, such that
    the annotation contains all relevant information for further analysis
    :param keywords: a list of all the keywords the utterances shall be searched for
    :param annotation_id: links the concrete annotation data to its meta-data (stores in annotations
    :param transcript_data: contains the whole transcript, i.e. meta-data and all utterances
    :return: a dict containing the annotationId and the processes utterances, such as
             tokenization and e.g. keyword detection
    """
    return {
        "annotationId": annotation_id,
        "transcriptId": transcript_data["_id"],
        "name": transcript_data["name"],
        "utterances": [{"isActionItem": ActionItemState.maybe.value}
                       for _ in transcript_data["transcript"]]
    }


async def add_transcript_annotation(annotation_data: AnnotationOut, corpus_id: PyObjectId):
    convert = partial(convert_transcript_to_annotation,
                      annotation_data.id)
    transcript_annotations = [convert(transcript) for transcript in
                              await retrieve_transcripts(corpus_id)]
    await transcript_annotation_collection.insert_many(transcript_annotations)


def format_transcript_annotation(transcript_annotation: dict) -> dict:
    return {
        "id": str(transcript_annotation["_id"]),
        "name": transcript_annotation["name"]
    }


async def retrieve_transcript_annotations(annotation_id: ObjectId) -> List[dict]:
    """
    :param annotation_id:
    :return: A list of all contained transcripts, with their respective meta-data
    """
    return [format_transcript_annotation(tran_ann) async for tran_ann in
            transcript_annotation_collection.find({"annotationId": annotation_id})]


async def retrieve_transcript_annotation(transcript_annotation_id: PyObjectId) -> dict:
    return await transcript_annotation_collection.find_one({"_id": transcript_annotation_id})


async def update_utterance_at_idx(transcript_annotation_id: PyObjectId, utterance: UtteranceAnnotationIn) -> None:
    await transcript_annotation_collection.update_one(
        {"_id": transcript_annotation_id},
        {"$set": {f"utterances.{utterance.idx}.content": {
            "isActionItem": str(utterance.isActionItem)
        }}})


async def update_transcript_annotation(transcript_annotation_id: PyObjectId,
                                       new_utterances: List[UtteranceAnnotationIn]) -> None:
    """
    Updates meta-data of all utterances at once
    :param transcript_annotation_id:
    :param new_utterances: list of all utterances of the new transcript
    :return:
    """
    json_utterances = jsonable_encoder(new_utterances)
    await transcript_annotation_collection.update_one(
        {"_id": transcript_annotation_id},
        {"$set": {"utterances": json_utterances}}
    )
