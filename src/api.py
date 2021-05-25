from fastapi import FastAPI

from routes import router as TranscriptRouter

app = FastAPI()

app.include_router(TranscriptRouter, tags=["Transcript"], prefix="/transcript")


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to this fantastic app!"}