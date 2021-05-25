from unittest import TestCase
import xml.etree.ElementTree as ET

from src.business_logic import parse_xml, format_utterance, parse_files, file_contains_transcript

ICSI_TEST_TRANSCRIPT_PATH = 'test_data/Bdb001.mrt'
ICSI_TEST_TRANSCRIPT_NO_PARTICIPANT = 'test_data/Bro011.mrt'

ICSI_2_TEXT_2_NO_TEXT = 'test_data/two_text_two_no_text.mrt'

TEST_UTTERANCE_NO_TEXT = """<Segment StartTime="0.000" EndTime="3.956" Participant="me018">
      <NonVocalSound Description="mike noise"/>
    </Segment>"""

TEST_UTTERANCE_TEXT = """<Segment StartTime="0.056" EndTime="1.861" Participant="me011">
      Yeah, we had a long discussion about
    </Segment>"""


class Test(TestCase):
    def test_format_utterance(self):
        res_no_text = format_utterance(ET.fromstring(TEST_UTTERANCE_NO_TEXT))
        self.assertEqual('me018', res_no_text["speaker"])
        self.assertEqual('', res_no_text["text"])

        res_text = format_utterance(ET.fromstring(TEST_UTTERANCE_TEXT))
        self.assertEqual('me011', res_text["speaker"])
        self.assertEqual('Yeah, we had a long discussion about', res_text["text"])

    def test_parse_xml(self):
        res_no_empty = parse_xml(ICSI_2_TEXT_2_NO_TEXT)
        self.assertEqual(2, len(res_no_empty["transcript"]))

        res_with_empty = parse_xml(ICSI_2_TEXT_2_NO_TEXT, keep_empty=True)
        self.assertEqual(4, len(res_with_empty["transcript"]))

    def test_parse_xml_no_participant(self):
        res = parse_xml(ICSI_TEST_TRANSCRIPT_NO_PARTICIPANT)
        self.assertIsInstance(res, dict)

    def test_parse_files(self):
        res = parse_files('test_data', parse_xml)
        self.assertEqual(3, len(res))

    def test_file_contains_transcript_neg_preambles(self):
        res = file_contains_transcript('data/ICSI/transcripts/preambles.mrt', '.mrt')
        self.assertFalse(res)

    def test_file_contains_transcript_neg_endswith_mrt(self):
        res = file_contains_transcript('data/ICSI/transcripts/preambles.txt', '.mrt')
        self.assertFalse(res)

    def test_file_contains_transcript(self):
        res = file_contains_transcript('data/ICSI/transcripts/Bro011.mrt', '.mrt')
        self.assertTrue(res)

