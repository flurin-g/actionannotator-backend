from typing import List

from fastapi import APIRouter

from src.api.helper import raise_if_none
from src.data_access.corpus import retrieve_corpora
from src.data_model.corpus import Corpus

router = APIRouter()


@router.get("/", response_model=List[Corpus])
async def get_corpora():
    return raise_if_none(await retrieve_corpora(), 404, "No corpora exist")
