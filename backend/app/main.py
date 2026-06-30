from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .schemas import EvalRequest, GoalRequest, MemoryRequest, RagIngestRequest, RagRequest, ReviewRequest
from .services.agent import PlannerAgent
from .services.evaluator import PlannerEvaluator
from .services.memory import MemoryStore
from .services.rag import RagIndex
from .services.tools import list_tools

app = FastAPI(title="MyNotes AI Planner API", version="0.2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

agent = PlannerAgent()
rag = RagIndex()
memory = MemoryStore()
evaluator = PlannerEvaluator()


@app.get("/api/health")
def health():
    return {"ok": True, "service": "mynotes-ai"}


@app.post("/api/agent/plan")
async def generate_plan(req: GoalRequest):
    return await agent.plan(req)


@app.post("/api/agent/review")
async def review_day(req: ReviewRequest):
    return await agent.review(req)


@app.post("/api/rag/query")
async def query_materials(req: RagRequest):
    return rag.query(req)


@app.post("/api/rag/ingest")
async def ingest_materials(req: RagIngestRequest):
    return rag.ingest(req)


@app.post("/api/memory/preferences")
async def save_preferences(req: MemoryRequest):
    return memory.save(req)


@app.get("/api/memory/preferences")
async def get_preferences(user_id: str = "local-user"):
    return memory.get(user_id)


@app.get("/api/agent/tools")
async def agent_tools():
    return list_tools()


@app.post("/api/eval/planner")
async def evaluate_planner(req: EvalRequest):
    return evaluator.run(req)
