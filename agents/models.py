"""Pydantic 모델 - Agent 입출력 스키마."""

from pydantic import BaseModel, Field


class IntentResult(BaseModel):
    """대화에서 추출된 의도."""

    intent: str = Field(description="create | list | update | delete | chat")
    summary: str | None = Field(default=None, description="일정 제목")
    start_time: str | None = Field(default=None, description="시작 시간 ISO 8601")
    end_time: str | None = Field(default=None, description="종료 시간 ISO 8601")
    description: str | None = Field(default=None, description="일정 설명")
    location: str | None = Field(default=None, description="장소")
    event_id: str | None = Field(default=None, description="수정/삭제 대상 이벤트 ID")
    date_range_start: str | None = Field(default=None, description="조회 시작일")
    date_range_end: str | None = Field(default=None, description="조회 종료일")
    raw_text: str = Field(default="", description="원본 사용자 입력")
    confidence: float = Field(default=0.0, description="추출 신뢰도 0~1")
