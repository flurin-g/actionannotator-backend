import asyncio
import os
import xml.etree.ElementTree as ET
from typing import List

from src.data_access.corpus import add_corpus

ICSI_TRANSCRIPT_PATH = 'data/ICSI/transcripts'


def file_contains_transcript(file, file_suffix) -> bool:
    return 'preambles' not in file and file.endswith(file_suffix)


def parse_files(basepath: str, parser: callable, file_suffix: str = '.mrt') -> List[dict]:
    return [parser(os.path.join(basepath, file)) for file in os.listdir(basepath) if
            file_contains_transcript(file, file_suffix)]


def format_utterance(utterance) -> dict:
    return {
        "speaker": utterance.attrib.get('Participant', 'Unknown'),
        "text": utterance.text.strip()
    }


def parse_xml(file_path: str, keep_empty: bool = False) -> dict:
    def keep_utterance(utterance) -> bool:
        return keep_empty or utterance.text.strip()

    meeting = ET.parse(file_path).getroot()
    transcript = meeting[1]

    return {
        "name": meeting.attrib["Session"],
        "transcript": [format_utterance(utterance) for utterance in transcript if keep_utterance(utterance)]
    }


async def init_corpus(name: str, parser: callable) -> None:
    # preprocess corpus
    corpus = {
        "name": name,
        "transcripts": parse_files(ICSI_TRANSCRIPT_PATH, parser)
    }
    await add_corpus(corpus)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(init_corpus("ICSI", parse_xml))

