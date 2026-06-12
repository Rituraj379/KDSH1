from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/api/agent", tags=["agent"])


class AgentMessage(BaseModel):
    message: str
    context: dict[str, Any] | None = None


@router.post("/chat")
def chat(payload: AgentMessage) -> dict[str, Any]:
    return {
        "reply": "AI agent hook is ready. Connect your model or agent service here.",
        "received": payload.message,
        "context": payload.context or {},
    }
