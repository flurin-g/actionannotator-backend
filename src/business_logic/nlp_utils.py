from typing import List

import nltk

tokenizer = nltk.word_tokenize


def nlp_pipeline(transcript: dict, keywords: list) -> list[dict]:
    def detect_keywords(utterance: list) -> List[str]:
        return [keyword for keyword in keywords if keyword in utterance]

    return [
        {
            "keywords": detect_keywords(tokenizer(utterance["text"].lower())),
            "isActionItem": "unknown"
        } for utterance in transcript
    ]
