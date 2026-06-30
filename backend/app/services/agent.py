import json

from ..db import load_memory, save_event
from ..schemas import GoalRequest, ReviewRequest
from .llm import LlmClient
from .tools import AGENT_TOOLS


class PlannerAgent:
    def __init__(self):
        self.llm = LlmClient()

    async def plan(self, req: GoalRequest):
        prompt = (
            "Create a practical AI planner output as JSON with keys summary, phases, "
            "tasks and rationale. Tasks must include time, text and reason.\n\n"
            f"Goal: {req.goal}\nDeadline: {req.deadline}\nDaily hours: {req.daily_hours}\n"
            f"Preferences: {req.preferences or load_memory()}\nContext: {req.context}"
        )
        raw = await self.llm.complete("You are an AI planning agent. Return strict JSON.", prompt)
        if raw:
            try:
                data = json.loads(raw)
                data["mode"] = "llm"
                data.setdefault("tool_calls", self._tool_calls())
                save_event("plan", json.dumps(data, ensure_ascii=False))
                return data
            except json.JSONDecodeError:
                pass
        data = self._mock_plan(req)
        save_event("plan", json.dumps(data, ensure_ascii=False))
        return data

    async def review(self, req: ReviewRequest):
        day = req.plans.get(req.date, {}) if req.plans else {}
        plans = day.get("plans", [])
        done = len([p for p in plans if p.get("done")])
        data = {
            "mode": "mock",
            "summary": f"Today completed {done}/{len(plans)} tasks.",
            "suggestions": [
                "Keep completed items as evidence for weekly review.",
                "Move unfinished work into smaller next actions.",
                "Adjust tomorrow's workload based on actual completion time.",
            ],
        }
        save_event("review", json.dumps(data, ensure_ascii=False))
        return data

    def _mock_plan(self, req: GoalRequest):
        goal = req.goal or "improve AI application development skills"
        return {
            "mode": "mock",
            "summary": f"Plan generated for {goal}, about {req.daily_hours} hours per day.",
            "phases": [
                {"title": "Phase 1: map the gap", "detail": "Compare target role requirements with current skills."},
                {"title": "Phase 2: build portfolio", "detail": "Ship AI app, Agent, RAG and deployment features."},
                {"title": "Phase 3: review and apply", "detail": "Track progress and refine resume wording."},
            ],
            "tasks": [
                {"time": "09:00", "text": "Analyze target JD and skill gaps", "reason": "Ground the plan in real hiring requirements."},
                {"time": "14:30", "text": "Implement one demonstrable AI feature", "reason": "Visible output improves resume credibility."},
                {"time": "20:00", "text": "Review today and adjust tomorrow", "reason": "Dynamic replanning creates a closed loop."},
            ],
            "rationale": "The agent uses goal, available time and materials to create an actionable loop.",
            "tool_calls": self._tool_calls(),
            "preferences_used": req.preferences or load_memory(),
        }

    def _tool_calls(self):
        return [
            {"tool": "search_materials", "input": {"query": "target JD and skill gaps", "top_k": 3}},
            {"tool": "create_task", "input": {"time": "09:00", "text": "Analyze target JD and skill gaps"}},
            {"tool": "create_task", "input": {"time": "14:30", "text": "Implement one demonstrable AI feature"}},
            {"tool": "summarize_week", "input": {"week_start": "auto", "week_end": "auto"}},
        ]
