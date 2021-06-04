from functools import partial
from unittest import TestCase

from src.data_access.transcript_annotation import convert_transcript_to_annotation

transcript = [
    {
        'speaker': 'mn007',
        'text': "I don't know. Do you have news from the conference talk?"
    },
    {
        'speaker': 'mn007',
        'text': 'programmed for yesterday -'
    },
    {
        'speaker': 'me013',
        'text': 'Uh -'
    },
    {
        'speaker': 'fn002',
        'text': 'Yesterday morning on video conference.'
    },

]


class Test(TestCase):
    def test_convert_transcript_to_annotation(self):
        convert = partial(convert_transcript_to_annotation,
                          annotation_id="666",
                          keywords=["programmed", "yesterday"])

        res = convert(transcript_data=transcript)

        self.assertListEqual(["programmed", "yesterday"],
                             res["utterances"][1]["keywords"])

        self.assertListEqual([],
                             res["utterances"][2]["keywords"])

        self.assertListEqual(["yesterday"],
                             res["utterances"][3]["keywords"])
