from ..services.auth import Auth


async def verify_token(token):
    token = token.split("Bearer ")[1]
    auth_service = Auth()
    await auth_service.get_token(token)
