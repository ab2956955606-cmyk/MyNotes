from dataclasses import dataclass
from uuid import uuid4

import httpx

from ..db import get_conn
from .ai_settings import EffectiveAiSettings, get_effective_ai_settings


@dataclass(frozen=True)
class LlmResult:
    content: str
    provider: str
    model: str


def _chat_completions_url(base_url: str) -> str:
    cleaned = base_url.rstrip("/")
    if cleaned.endswith("/v1"):
        return f"{cleaned}/chat/completions"
    return f"{cleaned}/v1/chat/completions"


def record_ai_run(
    feature: str,
    settings: EffectiveAiSettings,
    input_summary: str,
    output_summary: str = "",
    success: bool = True,
    error: str = "",
) -> None:
    with get_conn() as conn:
        conn.execute(
            """
            INSERT INTO ai_runs(
              id, feature, provider, model, input_summary, output_summary, success, error
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                str(uuid4()),
                feature,
                settings.provider,
                settings.model,
                input_summary[:4000],
                output_summary[:4000],
                int(success),
                error[:1000],
            ),
        )


class LlmClient:
    def __init__(self):
        self.settings = get_effective_ai_settings()

    def is_enabled(self) -> bool:
        return self.settings.provider != "mock" and self.settings.has_api_key

    def complete(self, feature: str, system: str, user: str) -> LlmResult | None:
        if not self.is_enabled():
            record_ai_run(feature, self.settings, user, success=True, output_summary="mock fallback")
            return None

        payload = {
            "model": self.settings.model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            "temperature": self.settings.temperature,
        }
        try:
            with httpx.Client(timeout=self.settings.timeout_seconds) as client:
                response = client.post(
                    _chat_completions_url(self.settings.base_url),
                    headers={"Authorization": f"Bearer {self.settings.api_key}"},
                    json=payload,
                )
                response.raise_for_status()
                content = response.json()["choices"][0]["message"]["content"]
        except Exception as exc:
            record_ai_run(feature, self.settings, user, success=False, error=str(exc))
            return None

        record_ai_run(feature, self.settings, user, output_summary=content, success=True)
        return LlmResult(content=content, provider=self.settings.provider, model=self.settings.model)
