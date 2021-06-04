from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from src.api.transcript_annotation import router
from src.data_access.annotation import add_annotation, retrieve_annotations
from src.data_access.transcript_annotation import retrieve_transcript_annotation
from src.data_model.all import ResponseModel, ErrorResponseModel
from src.data_model.annotation import AnnotationSchema

router = APIRouter()


@router.post("/", response_description="Annotation data added into the database")
async def add_annotation_data(annotation: AnnotationSchema = Body(...)):
    """
    By providing the annotation-data, an annotation linked to its respective
    corpus, i.e. all the utterances to be linked, is automatically created
    :param annotation: Provides base-corpus, keywords and name of the annotation
           to be created
    """
    annotation = jsonable_encoder(annotation)
    new_transcript = await add_annotation(annotation)
    return ResponseModel(new_transcript, "Transcript added successfully.")


@router.get("/", response_description="Annotation retrieved")
async def get_annotations():
    """
    Gets all annotations, regardless of corpus used.
    :return: The returned data is only the annotation
             meta-data, meaning it doesn't contain the individual
             transcripts and their respective text.
    """
    annotations = await retrieve_annotations()
    if annotations:
        return ResponseModel(annotations, "Annotations retrieved successfully")
    return ResponseModel(annotations, "Empty list returned")


@router.get("/{id}", response_description="Transcripts annotations retrieved")
async def get_annotation(annotation_id):
    """
    :param annotation_id: identifies the annotation of whom the contained transcripts
           shall be shown
    :return: Annotation meta-data as well as a list of oll the transcripts contained
    """
    transcript_annotation = await retrieve_transcript_annotation(annotation_id)

    if transcript_annotation:
        return ResponseModel(transcript_annotation)
    return ErrorResponseModel("An error occurred.", 404, "Annotation doesn't exist.")
