from typing import List

from src.data_access.mongo_connection import corpus_collection, transcript_collection
from src.data_model.corpus import BaseCorpus, Corpus


async def retrieve_corpora() -> List[Corpus]:
    return [Corpus(**corpus) async for corpus in corpus_collection.find()]


async def retrieve_corpus_by_name(base_corpus: BaseCorpus):
    corpora = await retrieve_corpora()
    return [corpus for corpus in corpora if BaseCorpus(corpus.name) == base_corpus][0]


async def add_corpus(corpus_data: dict) -> None:
    corpus = await corpus_collection.insert_one({"name": corpus_data["name"]})
    corpus_id = corpus.inserted_id

    await transcript_collection.insert_many(
        [{
            "corpusId": corpus_id,
            "name": transcript["name"],
            "transcript": transcript["transcript"]
        } for transcript in corpus_data["transcripts"]]
    )
