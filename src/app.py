from fastapi import FastAPI

from src.api.corpus import router as corpus_router
from src.api.annotation import router as annotation_router
from src.api.transcript_annotation import router as transcript_annotation_router
from src.api.download import router as download_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(corpus_router, tags=["Corpus"], prefix="/corpus")
app.include_router(annotation_router, tags=["Annotation"], prefix="/annotation")
app.include_router(transcript_annotation_router, tags=["TranscriptAnnotation"], prefix="/transcriptAnnotation")
app.include_router(download_router, tags=["Download"], prefix="/download")


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to this fantastic app!"}
