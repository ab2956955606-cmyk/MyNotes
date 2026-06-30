from typing import Any

from pydantic import BaseModel, Field


class GoalRequest(BaseModel):
    goal: str = ""
    deadline: str = ""
    daily_hours: float = 2
    context: str = ""
    preferences: str = ""
    date: str = ""
    plans: dict[str, Any] = Field(default_factory=dict)


class ReviewRequest(BaseModel):
    goal: str = ""
    context: str = ""
    preferences: str = ""
    date: str = ""
    plans: dict[str, Any] = Field(default_factory=dict)


class RagRequest(BaseModel):
    goal: str = ""
    context: str = ""
    date: str = ""
    plans: dict[str, Any] = Field(default_factory=dict)


class RagIngestRequest(BaseModel):
    title: str = "Untitled material"
    content: str


class MemoryRequest(BaseModel):
    user_id: str = "local-user"
    preferences: str = ""


class EvalRequest(BaseModel):
    goal: str = "Land an AI application internship"
    cases: list[str] = Field(default_factory=list)
