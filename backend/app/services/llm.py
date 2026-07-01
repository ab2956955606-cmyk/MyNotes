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


@dataclass(frozen=True)
class LlmError:
    message: str
    error_type: str  # auth_error | insufficient_balance | bad_model | bad_base_url | timeout | network_error | server_error | unknown
    status_code: int


def _chat_completions_url(base_url: str) -> str:
    cleaned = base_url.rstrip("/")
    if cleaned.endswith("/v1"):
        return f"{cleaned}/chat/completions"
    return f"{cleaned}/v1/chat/completions"


def _classify_http_error(status_code: int, body: str) -> LlmError:
    body_lower = body.lower() if body else ""
    if status_code == 401:
        return LlmError("API Key 无效或已过期", "auth_error", status_code)
    if status_code == 402:
        return LlmError("账户余额不足", "insufficient_balance", status_code)
    if status_code in (400, 404, 422):
        if "model" in body_lower:
            return LlmError("模型名不存在或不支持", "bad_model", status_code)
        return LlmError("请求参数错误，请检查 Base URL 和模型名", "bad_request", status_code)
    if status_code == 429:
        msg = body or "请求过于频繁，请稍后重试"
        return LlmError(msg, "rate_limited", status_code)
    if status_code >= 500:
        return LlmError("模型服务端错误，请稍后重试", "server_error", status_code)
    return LlmError(f"请求失败 (HTTP {status_code})", "unknown", status_code)


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

    def complete(
        self, feature: str, system: str, user: str
    ) -> tuple[LlmResult | None, LlmError | None]:
        """Returns (result, error). On success error is None; on failure result is None."""
        if not self.is_enabled():
            record_ai_run(feature, self.settings, user, success=True, output_summary="mock fallback")
            return (None, None)

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
                if response.status_code != 200:
                    body = response.text
                    llm_err = _classify_http_error(response.status_code, body)
                    record_ai_run(feature, self.settings, user, success=False, error=llm_err.message)
                    return (None, llm_err)

                content = response.json()["choices"][0]["message"]["content"]
        except httpx.TimeoutException:
            llm_err = LlmError("模型服务请求超时，请检查网络或增大超时时间", "timeout", 0)
            record_ai_run(feature, self.settings, user, success=False, error=llm_err.message)
            return (None, llm_err)
        except httpx.ConnectError:
            llm_err = LlmError("Base URL 无法连接，请检查地址是否正确", "bad_base_url", 0)
            record_ai_run(feature, self.settings, user, success=False, error=llm_err.message)
            return (None, llm_err)
        except httpx.RemoteProtocolError:
            llm_err = LlmError("模型服务协议错误，请检查 Base URL", "network_error", 0)
            record_ai_run(feature, self.settings, user, success=False, error=llm_err.message)
            return (None, llm_err)
        except (KeyError, IndexError, ValueError) as exc:
            llm_err = LlmError(f"模型返回格式异常: {exc}", "parse_error", 0)
            record_ai_run(feature, self.settings, user, success=False, error=llm_err.message)
            return (None, llm_err)
        except Exception as exc:
            llm_err = LlmError(f"请求异常: {exc}", "unknown", 0)
            record_ai_run(feature, self.settings, user, success=False, error=str(exc))
            return (None, llm_err)

        record_ai_run(feature, self.settings, user, output_summary=content, success=True)
        return (LlmResult(content=content, provider=self.settings.provider, model=self.settings.model), None)
