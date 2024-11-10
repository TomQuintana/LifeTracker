from fastapi import HTTPException


def success_book_deleted(detail: str = "Book deleted successfully"):
    return {"message": detail}


def alert_not_found_resource(detail: str = "Resource not found"):
    raise HTTPException(status_code=404, detail=detail)


def bad_request(detail: str = "Bad request"):
    raise HTTPException(status_code=400, detail=detail)


def alert_book(detail: str = "Resource not found", status_code: int = 404):
    raise HTTPException(status_code=status_code, detail=detail)
