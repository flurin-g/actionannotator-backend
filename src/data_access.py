import motor.motor_asyncio
from bson.objectid import ObjectId

MONGO_DETAILS = "mongodb://localhost:27017"

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.icsi

transcript_collection = database.get_collection("icsi")


def transcript_helper(transcript) -> dict:
    return {
        "id": str(transcript["_id"]),
        "speaker": transcript["speaker"],
        "text": transcript["text"],
        "actionDetected": transcript["actionDetected"],
        "truePositive": transcript["truePositive"],
    }


# Retrieve all transcripts present in the database
async def retrieve_transcripts():
    transcripts = []
    async for transcript in transcript_collection.find():
        transcripts.append(transcript_helper(transcript))
    return transcripts


# Add a new transcript into to the database
async def add_transcript(transcript_data: dict) -> dict:
    transcript = await transcript_collection.insert_one(transcript_data)
    new_transcript = await transcript_collection.find_one({"_id": transcript.inserted_id})
    return transcript_helper(new_transcript)


# Retrieve a transcript with a matching ID
async def retrieve_transcript(transcript_id: str) -> dict:
    transcript = await transcript_collection.find_one({"_id": ObjectId(transcript_id)})
    if transcript:
        return transcript_helper(transcript)


# Update a transcript with a matching ID
async def update_transcript(transcript_id: str, data: dict):
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


# Delete a transcript from the database
async def delete_transcript(id: str):
    student = await student_collection.find_one({"_id": ObjectId(id)})
    if student:
        await student_collection.delete_one({"_id": ObjectId(id)})
        return True
