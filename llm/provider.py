"""litellm 기반 LLM 추상화 계층."""

import json
import litellm

from config.settings import settings
from config.llm_config import MAX_TOKENS, LLM_TIMEOUT

# litellm 로깅 최소화
litellm.suppress_debug_info = True


async def chat_completion(
    messages: list[dict],
    temperature: float = 0.7,
    response_format: dict | None = None,
    model: str | None = None,
) -> str:
    """LLM에 메시지를 보내고 응답을 받는다.

    Args:
        messages: 대화 메시지 리스트 [{"role": "...", "content": "..."}]
        temperature: 응답 다양성 (0.0~1.0)
        response_format: JSON mode 활성화 시 {"type": "json_object"}
        model: 모델 오버라이드 (None이면 설정 사용)

    Returns:
        LLM 응답 텍스트
    """
    model_name = model or settings.get_litellm_model()

    kwargs = {
        "model": model_name,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": MAX_TOKENS,
        "timeout": LLM_TIMEOUT,
    }

    if response_format:
        kwargs["response_format"] = response_format

    response = await litellm.acompletion(**kwargs)
    return response.choices[0].message.content


async def chat_completion_json(
    messages: list[dict],
    temperature: float = 0.0,
    model: str | None = None,
) -> dict:
    """LLM에 메시지를 보내고 JSON 응답을 파싱하여 반환한다."""
    text = await chat_completion(
        messages=messages,
        temperature=temperature,
        response_format={"type": "json_object"},
        model=model,
    )
    return json.loads(text)
