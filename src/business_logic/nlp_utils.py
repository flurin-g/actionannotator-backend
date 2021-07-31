from typing import List

import nltk

from src.data_model.transcript_annotation import ActionItemState

tokenizer = nltk.word_tokenize


def nlp_pipeline(transcript: dict) -> list[dict]:

    return [{"isActionItem": ActionItemState.maybe.value} for _ in transcript]
