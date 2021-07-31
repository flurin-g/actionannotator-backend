from datetime import datetime
from typing import List

from fastapi.encoders import jsonable_encoder

from src.data_access.corpus import retrieve_corpus_by_name
from src.data_access.mongo_connection import annotation_collection
from src.data_access.transcript_annotation import add_transcript_annotation
from src.data_model.annotation import AnnotationIn, AnnotationOut
from src.data_model.mongo_base import PyObjectId


async def add_annotation(annotation_data: AnnotationIn) -> AnnotationOut:
    annotation_data_with_date = jsonable_encoder(annotation_data)
    annotation_data_with_date["date"] = datetime.now().isoformat("T", "seconds")
    annotation = await annotation_collection.insert_one(annotation_data_with_date)
    annotation_out = AnnotationOut(**await annotation_collection.find_one({"_id": annotation.inserted_id}))
    corpus = await retrieve_corpus_by_name(annotation_out.baseCorpus)
    await add_transcript_annotation(annotation_out, corpus.id)

    return annotation_out


async def delete_annotation(annotation_id: PyObjectId):
    annotation_collection.delete_one({"_id": annotation_id})


async def retrieve_annotations() -> List[AnnotationOut]:
    return [
        AnnotationOut(**annotation)
        async for annotation in annotation_collection.find()
    ]


async def retrieve_annotation(annotation_id: PyObjectId) -> AnnotationOut:
    annotation = await annotation_collection.find_one({"_id": annotation_id})
    return AnnotationOut(**annotation)
