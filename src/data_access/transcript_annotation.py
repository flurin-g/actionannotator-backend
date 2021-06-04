from functools import partial
from typing import List

from bson import ObjectId

from src.business_logic.nlp_utils import nlp_pipeline
from src.data_access.mongo_connection import transcript_annotation_collection
from src.data_access.transcript import retrieve_transcripts


def convert_transcript_to_annotation(annotation_id: str, keywords: List[str], transcript_data: dict) -> dict:
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
        "transcriptId": str(transcript_data["_id"]),
        "name": transcript_data["name"],
        "utterances": nlp_pipeline(transcript_data["transcript"], keywords)
    }


async def add_transcript_annotation(annotation, annotation_data, corpus):
    convert = partial(convert_transcript_to_annotation,
                      annotation.inserted_id,
                      annotation_data["keywords"])
    transcript_annotations = [convert(transcript) for transcript in
                              await retrieve_transcripts(corpus["corpusId"])]
    await transcript_annotation_collection.insert_many(transcript_annotations)


def format_transcript_annotation(transcript_annotation: dict) -> dict:
    return {
        "transcriptAnnotationId": str(transcript_annotation["_id"]),
        "name": transcript_annotation["name"]
    }


async def retrieve_transcript_annotations(annotation_id: str) -> List[dict]:
    """
    :param annotation_id:
    :return: A list of all contained transcripts, with their respective meta-data
    """
    return [format_transcript_annotation(tran_ann) async for tran_ann in
            transcript_annotation_collection.find({"annotationId": ObjectId(annotation_id)})]


async def retrieve_transcript_annotation(transcript_annotation_id: str) -> dict:
    return await transcript_annotation_collection.find_one({"_id": ObjectId(transcript_annotation_id)})
