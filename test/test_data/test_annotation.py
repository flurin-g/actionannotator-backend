from datetime import datetime
from unittest import TestCase

from bson import ObjectId
from fastapi.encoders import jsonable_encoder

from src.data_model.annotation import AnnotationIn, AnnotationOut, Annotation


class TestAnnotationIn(TestCase):
    def setUp(self):
        self.annotation_dict = {
            "name": "some name",
            "date": "2011-10-05T14:48:00",
            "baseCorpus": "ICSI",
            "keywords": ["key", "words"]
        }

    def test_annotation_in_creation(self):
        annotation_in_model = AnnotationIn(**self.annotation_dict)
        self.assertIsInstance(annotation_in_model.date, datetime)
        self.assertTrue(not hasattr(annotation_in_model, "id"))

    def test_annotation_in_date_to_str(self):
        annotation_in_model = AnnotationIn(**self.annotation_dict)
        annotation_in_json = jsonable_encoder(annotation_in_model)
        self.assertIsInstance(annotation_in_model.date, datetime)
        self.assertIsInstance(annotation_in_json["date"], str)


class TestAnnotationOut(TestCase):
    def setUp(self):
        self.annotation_dict = {
            "_id": ObjectId(),
            "name": "some name",
            "date": "2011-10-05T14:48:00",
            "baseCorpus": "ICSI",
            "keywords": ["key", "words"]
        }

    def test_annotation_out_rename_id(self):
        annotation_out_model = AnnotationOut(**self.annotation_dict)
        self.assertTrue(hasattr(annotation_out_model, "id"))

    def test_annotation_out_id_to_str(self):
        annotation_out_model = AnnotationOut(**self.annotation_dict)
        annotation_out_json = jsonable_encoder(annotation_out_model)
        self.assertIsInstance(annotation_out_json["id"], str)
