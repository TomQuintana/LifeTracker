from fastapi import HTTPException


def not_found_resource(detail: str = "Resource not found"):
    raise HTTPException(status_code=404, detail=detail)


def bad_request(detail: str = "Bad request"):
    raise HTTPException(status_code=400, detail=detail)
