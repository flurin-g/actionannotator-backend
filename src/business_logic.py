import os
import xml.etree.ElementTree as ET
from typing import List

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
        "session": meeting.attrib["Session"],
        "transcript": [format_utterance(utterance) for utterance in transcript if keep_utterance(utterance)]
    }


#def init_icsi():
#    sessions = parse_files(ICSI_TRANSCRIPT_PATH, parse_xml)
#    session_ids = insert_into_icsi(sessions)
    # ToDo: session_ids needs to be stored, to access sessions (interviews by their ids
    #       consider using an object for that


if __name__ == '__main__':
    res = parse_files(ICSI_TRANSCRIPT_PATH, parse_xml)[0]
    for segment in res["transcript"]:
        print(segment)
