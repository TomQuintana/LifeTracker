from uuid import UUID

from ..services.auth import Auth


def decoded_user_id(token: str) -> UUID:
    auth_service = Auth()
    token_decoded = auth_service.check_payload(token)
    user_id = token_decoded.get("user_id")
    return user_id
