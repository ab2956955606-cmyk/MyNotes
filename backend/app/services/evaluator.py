from ..schemas import EvalRequest


DEFAULT_CASES = [
    "User has only 1 hour per day and a 30-day deadline.",
    "User missed two tasks and needs a lighter tomorrow plan.",
    "User uploaded a JD requiring Agent, RAG and FastAPI.",
    "User prefers deep work in the morning and review at night.",
    "User needs a weekly review with measurable outputs.",
]


class PlannerEvaluator:
    def run(self, req: EvalRequest):
        cases = req.cases or DEFAULT_CASES
        results = []
        for case in cases:
            score = self._score_case(case)
            results.append({
                "case": case,
                "score": score,
                "reason": self._reason(score),
            })
        avg = round(sum(item["score"] for item in results) / len(results), 2)
        return {
            "average_score": avg,
            "criteria": ["actionable", "time-aware", "adaptive", "context-grounded", "reviewable"],
            "results": results,
        }

    def _score_case(self, case: str) -> int:
        score = 3
        lowered = case.lower()
        if any(word in lowered for word in ["hour", "deadline", "morning", "night"]):
            score += 1
        if any(word in lowered for word in ["jd", "rag", "agent", "fastapi", "missed", "review"]):
            score += 1
        return min(score, 5)

    def _reason(self, score: int) -> str:
        if score >= 5:
            return "Covers context, time constraints and review loop."
        if score == 4:
            return "Mostly useful, but needs more measurable outputs."
        return "Needs stronger grounding and adaptation."
