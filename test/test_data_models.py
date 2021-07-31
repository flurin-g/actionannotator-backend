from datetime import datetime
from unittest import TestCase

from bson import ObjectId
from fastapi.encoders import jsonable_encoder

from src.data_model.annotation import Annotation
from src.data_model.corpus import BaseCorpus
from src.data_model.transcript_annotation import TranscriptAnnotationOut


class TestAnnotationModel(TestCase):
    def setUp(self):
        self.annotation_dict = {
            "name": "some name",
            "date": "2011-10-05T14:48:00",
            "baseCorpus": "ICSI",
            "keywords": ["key", "words"]
        }

    def test_annotation_from_api(self):
        annotation_model = Annotation(**self.annotation_dict)
        self.assertIsInstance(annotation_model.date, datetime)

        annotation_dict = jsonable_encoder(annotation_model)
        self.assertEqual("2011-10-05T14:48:00", annotation_dict["date"])

    def test_annotation_from_api_bad_id(self):
        self.annotation_dict["id"] = "foobar"
        with self.assertRaises(ValueError):
            Annotation(**self.annotation_dict)

    def test_annotation_from_db(self):
        self.annotation_dict["_id"] = ObjectId()
        annotation_model = Annotation(**self.annotation_dict)

        self.assertTrue(hasattr(annotation_model, 'id'))
        self.assertIsInstance(annotation_model.id, ObjectId)
        self.assertIsInstance(annotation_model.date, datetime)
        self.assertIsInstance(annotation_model.baseCorpus, BaseCorpus)


class TestTranscriptAnnotationModel(TestCase):
    def setUp(self):
        self.annotation_transcript_dict = {
            "annotationId": ObjectId(),
            "transcriptId": ObjectId(),
            "name": "testTranscriptAnnotation"
        }
        self.utterances = [
            {
                "idx": 0,
                "isActionItem": "maybe"
            },
            {
                "idx": 1,
                "isActionItem": "no"
            }
        ]

    def test_transcript_annotation(self):
        self.annotation_transcript_dict["utterances"] = self.utterances

        transcript_annotation = TranscriptAnnotationOut(**self.annotation_transcript_dict)
        print(jsonable_encoder(transcript_annotation))
