import motor.motor_asyncio

MONGO_URL = "mongodb://localhost:27017"

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URL)
database = client.annotater

corpus_collection = database.get_collection("corpus")
transcript_collection = database.get_collection("transcript")
annotation_collection = database.get_collection("annotation")
transcript_annotation_collection = database.get_collection("transcriptAnnotation")
