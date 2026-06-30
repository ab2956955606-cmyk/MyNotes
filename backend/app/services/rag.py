import re
from collections import Counter

from ..db import load_rag_chunks, save_rag_chunk
from ..schemas import RagIngestRequest, RagRequest


def tokenize(text: str) -> list[str]:
    return re.findall(r"[\w\u4e00-\u9fff]+", text.lower())


class RagIndex:
    def ingest(self, req: RagIngestRequest):
        chunks = [c.strip() for c in re.split(r"\n{2,}|[。.!?]", req.content or "") if c.strip()]
        for chunk in chunks:
            save_rag_chunk(req.title, chunk)
        return {
            "ok": True,
            "title": req.title,
            "chunks": len(chunks),
        }

    def query(self, req: RagRequest):
        inline_chunks = [
            {"title": "Inline context", "chunk": c.strip()}
            for c in re.split(r"\n{2,}|[。.!?]", req.context or "")
            if c.strip()
        ]
        chunks = inline_chunks + load_rag_chunks()
        if not chunks:
            chunks = [{"title": "Empty material", "chunk": "No material provided. Paste a JD, course note, or resume to enable retrieval."}]
        query_terms = Counter(tokenize(req.goal + " " + req.date))
        scored = []
        for idx, item in enumerate(chunks):
            terms = Counter(tokenize(item["chunk"]))
            score = sum((query_terms & terms).values()) or (1 if idx == 0 else 0)
            scored.append((score, idx, item))
        top = sorted(scored, reverse=True)[:3]
        return {
            "mode": "rag-lite",
            "answer": "Retrieved the most relevant material snippets for planning.",
            "sources": [
                {"title": item["title"], "quote": item["chunk"][:220]}
                for _, _, item in top
            ],
        }
