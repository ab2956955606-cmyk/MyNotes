from ..db import load_memory, save_memory
from ..schemas import MemoryRequest


class MemoryStore:
    def save(self, req: MemoryRequest):
        save_memory(req.user_id, req.preferences)
        return {
            "ok": True,
            "user_id": req.user_id,
            "preferences": req.preferences,
        }

    def get(self, user_id: str = "local-user"):
        return {
            "user_id": user_id,
            "preferences": load_memory(user_id),
        }
