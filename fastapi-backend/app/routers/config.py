import os

from fastapi import APIRouter

router = APIRouter(prefix="/api/config", tags=["config"])


@router.get("/paypal")
def paypal_client_id() -> str:
    return os.getenv("PAYPAL_CLIENT_ID", "sb")
