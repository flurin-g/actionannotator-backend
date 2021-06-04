from fastapi import APIRouter

from src.data_access.corpus import retrieve_corpora
from src.data_model.all import ResponseModel

router = APIRouter()


@router.get("/", response_description="Transcript retrieved")
async def get_corpora():
    corpora = await retrieve_corpora()
    if corpora:
        return ResponseModel(corpora, "Corpora data retrieved successfully")
    return ResponseModel(corpora, "Empty list returned")
