import json
import os
import shutil
from pathlib import Path
from shutil import make_archive

from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import FileResponse
from starlette.background import BackgroundTasks

from src.api.transcript_annotation import fetch_annotated_transcript
from src.data_access.annotation import retrieve_annotation
from src.data_access.transcript_annotation import retrieve_transcript_annotations
from src.data_model.mongo_base import PyObjectId

router = APIRouter()


def remove_file(path: str) -> None:
    os.unlink(path)


def remove_folder(path: str) -> None:
    shutil.rmtree(path)


@router.get("/{annotation_id}", response_class=FileResponse)
async def download_annotation(annotation_id: PyObjectId, background_tasks: BackgroundTasks):
    annotation = await retrieve_annotation(annotation_id)
    transcript_annotations = await retrieve_transcript_annotations(annotation_id)

    base = Path(f'../data/{annotation.name}')
    base.mkdir(exist_ok=True)

    for transcript_annotation in jsonable_encoder(transcript_annotations):
        annotated_transcript = await fetch_annotated_transcript(PyObjectId(transcript_annotation["id"]))
        annotated_transcript_path = base / (annotated_transcript["name"] + ".json")
        annotated_transcript_path.write_text(json.dumps(annotated_transcript["utterances"]))

    archive_name = make_archive(base, 'zip', root_dir=base)

    background_tasks.add_task(remove_file, archive_name)
    background_tasks.add_task(remove_folder, base)

    return FileResponse(archive_name, media_type="application/zip", filename=f'{annotation.name}.zip')
