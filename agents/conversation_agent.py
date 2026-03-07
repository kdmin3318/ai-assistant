"""Conversation Agent - 한국어 의도/엔티티 추출."""

from datetime import datetime
from zoneinfo import ZoneInfo

from agents.base import BaseAgent
from config.settings import settings
from llm.provider import chat_completion_json
from llm.prompts import INTENT_EXTRACTION_PROMPT
from agents.models import IntentResult


class ConversationAgent(BaseAgent):
    """사용자 입력에서 일정 관련 의도와 엔티티를 추출하는 에이전트."""

    def __init__(self):
        super().__init__("ConversationAgent")

    async def process(self, user_input: str) -> dict:
        """사용자 입력을 분석하여 구조화된 의도를 반환한다."""
        tz = ZoneInfo(settings.timezone)
        now = datetime.now(tz)

        system_prompt = INTENT_EXTRACTION_PROMPT.format(
            current_time=now.isoformat(),
            timezone=settings.timezone,
        )

        messages = [
            {"role": "system", "content": system_prompt},
            *self.conversation_history,
            {"role": "user", "content": user_input},
        ]

        result = await chat_completion_json(messages=messages)

        # raw_text 보정
        result["raw_text"] = user_input

        # Pydantic 검증
        intent = IntentResult(**result)
        return intent.model_dump()
