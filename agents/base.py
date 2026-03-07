"""BaseAgent 추상 클래스."""

from abc import ABC, abstractmethod


class BaseAgent(ABC):
    """모든 에이전트의 기본 클래스."""

    def __init__(self, name: str):
        self.name = name
        self.conversation_history: list[dict] = []

    def add_message(self, role: str, content: str):
        """대화 히스토리에 메시지를 추가한다."""
        self.conversation_history.append({"role": role, "content": content})

    def clear_history(self):
        """대화 히스토리를 초기화한다."""
        self.conversation_history.clear()

    @abstractmethod
    async def process(self, user_input: str) -> dict:
        """사용자 입력을 처리하고 결과를 반환한다.

        Returns:
            처리 결과 딕셔너리
        """
        ...
