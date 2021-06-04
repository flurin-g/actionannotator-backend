from functools import partial
from typing import List

from src.business_logic.nlp_utils import nlp_pipeline
from src.data_access.mongo_connection import transcript_annotation_collection
from src.data_access.transcript import retrieve_transcripts


def convert_transcript_to_annotation(annotation_id: str, keywords: List[str], transcript_data: dict) -> dict:
    """
    This function injects the nlp-processing into the data-persistence step, such that
    the annotation contains all relevant information for further analysis
    :param keywords: a list of all the keywords the utterances shall be searched for
    :param annotation_id: links the concrete annotation data to its meta-data (stores in annotations
    :param transcript_data: contains the whole transcript, i.e. all utterances
    :return: a dict containing the annotationId and the processes utterances, such as
             tokenization and e.g. keyword detection
    """
    return {
        "annotationId": annotation_id,
        "utterances": nlp_pipeline(transcript_data, keywords)
    }


async def add_transcript_annotation(annotation, annotation_data, corpus):
    convert = partial(convert_transcript_to_annotation,
                      annotation.inserted_id,
                      annotation_data["keywords"])
    transcript_annotations = [convert(transcript["transcript"]) for transcript in
                              await retrieve_transcripts(corpus["corpusId"])]
    await transcript_annotation_collection.insert_many(transcript_annotations)


async def retrieve_transcript_annotation(annotation_id):
    """
    :param annotation_id:
    :return: annotation meta-data for a single annotation, and a list of all
             contained transcripts, with their respective meta-data as well
    """
    transcript_annotation = transcript_annotation_collection.find_one()

