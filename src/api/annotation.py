from typing import List

from fastapi import APIRouter, Body, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import FileResponse

from src.api.helper import raise_if_none
from src.data_access.annotation import add_annotation, retrieve_annotations, retrieve_annotation, delete_annotation
from src.data_access.transcript_annotation import retrieve_transcript_annotations
from src.data_model.annotation import AnnotationOut, AnnotationIn
from src.data_model.mongo_base import PyObjectId

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=AnnotationOut, response_model_exclude_unset=True)
async def add_annotation_data(annotation: AnnotationIn = Body(...)):
    """
    By providing the annotation-data, an annotation linked to its respective
    corpus, i.e. all the utterances to be linked, is automatically created
    :param annotation: Provides base-corpus, keywords and name of the annotation
           to be created
    """
    return raise_if_none(await add_annotation(annotation), 422, "The specified corpus is not valid")


file_path = "../data/ISL.zip"


@router.get("/", response_model=List[AnnotationOut], response_model_exclude_unset=True)
async def get_annotations():
    """
    Gets all annotations, regardless of corpus used.
    :return: The returned data is only the annotation
             meta-data, meaning it doesn't contain the individual
             transcripts and their respective text.
    """
    return raise_if_none(await retrieve_annotations(), 204, "No Annotations exist")


@router.get("/{annotation_id}", response_model=AnnotationOut)
async def get_annotation(annotation_id: PyObjectId):
    """
    :param annotation_id: identifies the annotation of whom the contained transcripts
           shall be shown
    :return: Annotation meta-data as well as a list of oll the transcripts contained
    """
    annotation = await retrieve_annotation(annotation_id)
    annotation.transcripts = await retrieve_transcript_annotations(annotation_id)

    return raise_if_none(annotation, 404, "Annotation not found")


@router.delete("/{annotation_id}")
async def delete_annotation_data(annotation_id: PyObjectId):
    await delete_annotation(annotation_id)
    return raise_if_none(await retrieve_annotations(), 204, "No Annotations exist")
