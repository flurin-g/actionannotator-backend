from typing import List

from src.data_access.mongo_connection import corpus_collection, transcript_collection


async def retrieve_corpora():
    return [{"corpusId": str(corpus["_id"]), "name": corpus["name"]} async for corpus in corpus_collection.find()]


async def retrieve_corpus_by_name(name: str):
    corpora = await retrieve_corpora()
    return [corpus for corpus in corpora if corpus["name"] == name][0]


async def add_corpus(corpus_data: dict) -> None:
    corpus = await corpus_collection.insert_one({"name": corpus_data["name"]})
    corpus_id = corpus.inserted_id

    await transcript_collection.insert_many(
        [{
            "corpusId": str(corpus_id),
            "name": transcript["name"],
            "transcript": transcript["transcript"]
        } for transcript in corpus_data["transcripts"]]
    )
