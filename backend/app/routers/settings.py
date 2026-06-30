from fastapi import APIRouter

from ..schemas import AiSettingsOut, AiSettingsTestOut, AiSettingsTestPayload, AiSettingsUpdate
from ..services.ai_settings import get_public_ai_settings, save_ai_settings
from ..services.llm import LlmClient

router = APIRouter(prefix="/api/ai", tags=["ai-settings"])


@router.get("/settings", response_model=AiSettingsOut)
def read_ai_settings() -> AiSettingsOut:
    return get_public_ai_settings()


@router.put("/settings", response_model=AiSettingsOut)
def update_ai_settings(payload: AiSettingsUpdate) -> AiSettingsOut:
    return save_ai_settings(payload)


@router.post("/test", response_model=AiSettingsTestOut)
def test_ai_settings(payload: AiSettingsTestPayload) -> AiSettingsTestOut:
    client = LlmClient()
    if not client.is_enabled():
        return AiSettingsTestOut(
            ok=True,
            mode="mock",
            message="Mock mode is active. Add an API key to test a real model.",
            provider=client.settings.provider,
            model=client.settings.model,
        )
    result = client.complete(
        "settings_test",
        "You are a concise health-check assistant. Reply in one short sentence.",
        payload.prompt,
    )
    if result:
        return AiSettingsTestOut(
            ok=True,
            mode="llm",
            message=result.content,
            provider=result.provider,
            model=result.model,
        )
    return AiSettingsTestOut(
        ok=False,
        mode="error",
        message="The model call failed. Check provider, base URL, model, and API key.",
        provider=client.settings.provider,
        model=client.settings.model,
    )
