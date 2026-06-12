from typing import Any

from fastapi import Header, HTTPException

from .security import decode_access_token
from .store import load_store, public_user


def current_user(authorization: str | None = Header(default=None)) -> dict[str, Any]:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="No token")

    payload = decode_access_token(authorization.removeprefix("Bearer ").strip())
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    store = load_store()
    user = next((item for item in store["users"] if item["_id"] == payload.get("_id")), None)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")

    return public_user(user)
