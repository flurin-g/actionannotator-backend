from fastapi import HTTPException


def raise_if_none(resource, status_code: int, msg: str):
    if not resource:
        raise HTTPException(status_code, detail=msg)
    return resource
