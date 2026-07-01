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
        if client.settings.provider == "mock":
            return AiSettingsTestOut(
                ok=True,
                mode="mock",
                message="当前是 Mock 模式，不需要 API Key。配置真实 Key 即可调用模型。",
                provider=client.settings.provider,
                model=client.settings.model,
            )
        return AiSettingsTestOut(
            ok=False,
            mode="error",
            message="API Key 未保存，请在设置中填入 API Key",
            provider=client.settings.provider,
            model=client.settings.model,
            error_type="no_key",
        )

    result, err = client.complete(
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
        message=err.message if err else "模型调用失败，请检查设置",
        provider=client.settings.provider,
        model=client.settings.model,
        error_type=err.error_type if err else "unknown",
        status_code=err.status_code if err else 0,
    )
