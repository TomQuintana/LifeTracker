from fastapi import HTTPException


def alert_not_found_resource(detail: str = "Resource not found"):
    raise HTTPException(status_code=404, detail=detail)


def bad_request(detail: str = "Bad request"):
    raise HTTPException(status_code=400, detail=detail)


def success_book_deleted(detail: str = "Book deleted successfully"):
    return {"message": detail}
