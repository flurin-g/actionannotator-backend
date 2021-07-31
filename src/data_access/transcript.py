from bson.objectid import ObjectId

from src.data_access.mongo_connection import transcript_collection
from src.data_model.mongo_base import PyObjectId


def transcript_helper(transcript) -> dict:
    return {
        "id": transcript["_id"],
        "speaker": transcript["speaker"],
        "text": transcript["text"],
        "actionDetected": transcript["actionDetected"],
        "truePositive": transcript["truePositive"],
    }


async def retrieve_transcripts(corpus_id: PyObjectId):
    return [transcript async for transcript in transcript_collection.find({"corpusId": corpus_id})]


async def add_transcript(transcript_data: dict) -> dict:
    transcript = await transcript_collection.insert_one(transcript_data)
    new_transcript = await transcript_collection.find_one({"_id": transcript.inserted_id})
    return transcript_helper(new_transcript)


async def retrieve_transcript(transcript_id: str) -> dict:
    return await transcript_collection.find_one({"_id": ObjectId(transcript_id)})


async def update_transcript(transcript_id: str, data: dict) -> bool:
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    transcript = await transcript_collection.find_one({"_id": ObjectId(transcript_id)})
    if transcript:
        updated_transcript = await transcript_collection.update_one(
            {"_id": ObjectId(transcript_id)}, {"$set": data}
        )
        if updated_transcript:
            return True
        return False


async def delete_transcript(transcript_id: str):
    student = await transcript_collection.find_one({"_id": ObjectId(transcript_id)})
    if student:
        await transcript_collection.delete_one({"_id": ObjectId(transcript_id)})
        return True
