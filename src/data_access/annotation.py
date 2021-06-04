from src.data_access.corpus import retrieve_corpus_by_name
from src.data_access.mongo_connection import annotation_collection
from src.data_access.transcript_annotation import add_transcript_annotation


async def add_annotation(annotation_data: dict) -> dict:
    annotation = await annotation_collection.insert_one(annotation_data)

    corpus = await retrieve_corpus_by_name(annotation_data["baseCorpus"])
    await add_transcript_annotation(annotation, annotation_data, corpus)

    return {"annotationId": str(annotation.inserted_id)}


async def retrieve_annotations():
    return [
        {
            "annotationId": str(annotation["_id"]),
            "name": annotation["name"],
            "data": annotation["date"],
            "baseCorpus": annotation["baseCorpus"],
            "keywords": annotation["keywords"]
        }
        async for annotation in annotation_collection.find()
    ]
