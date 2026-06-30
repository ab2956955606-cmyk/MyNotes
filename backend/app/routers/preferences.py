from fastapi import APIRouter

from ..schemas import MemoryPayload
from ..services.memory import MemoryStore

router = APIRouter(prefix="/api/memory", tags=["memory"])

memory = MemoryStore()


@router.post("/preferences")
def save_preferences(payload: MemoryPayload) -> dict[str, str]:
    return memory.save(payload)


@router.get("/preferences")
def get_preferences(user_id: str = "local-user") -> dict[str, str]:
    return memory.get(user_id)
