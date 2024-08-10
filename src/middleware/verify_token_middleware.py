from ..services.auth import Auth
from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse


async def verify_token(token: str):
    token = token.split("Bearer ")[1]
    auth_service = Auth()
    try:
        await auth_service.get_token(token)
    except HTTPException as e:
        raise e


async def verify_token_middleware(request: Request, call_next):
    protected_routes = ["/api/books"]
    token = request.headers.get("Authorization")

    if any(request.url.path.startswith(route) for route in protected_routes):
        if not token:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Authorization token is missing"},
                headers={"WWW-Authenticate": "Bearer"},
            )

        try:
            test = await verify_token(token)
            print("test", test)
        except HTTPException as error:
            return JSONResponse(
                status_code=error.status_code,
                content={"detail": error.detail},
                headers=error.headers,
            )

    response = await call_next(request)
    return response
