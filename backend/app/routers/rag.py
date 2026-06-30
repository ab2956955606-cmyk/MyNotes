from fastapi import APIRouter

from ..schemas import AiPayload, RagIngestPayload
from ..services.rag import RagService

router = APIRouter(prefix="/api/rag", tags=["rag"])

rag = RagService()


@router.post("/ingest")
def rag_ingest(payload: RagIngestPayload) -> dict[str, int | str]:
    return rag.ingest(payload)


@router.post("/query")
def rag_query(payload: AiPayload) -> dict[str, object]:
    return rag.query(payload)
