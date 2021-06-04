from fastapi import FastAPI

from src.api.corpus import router as corpus_router
from src.api.transcript import router as transcript_router
from src.api.annotation import router as annotation_router
from src.api.transcript_annotation import router as transcript_annotation_router

app = FastAPI()

app.include_router(corpus_router, tags=["Corpus"], prefix="/corpus")
app.include_router(transcript_router, tags=["Transcript"], prefix="/transcript")
app.include_router(annotation_router, tags=["Annotation"], prefix="/annotation")
app.include_router(transcript_annotation_router, tags=["TranscriptAnnotation"], prefix="/transcriptAnnotation")


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to this fantastic app!"}
