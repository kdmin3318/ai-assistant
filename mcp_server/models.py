"""Pydantic 모델 - MCP 도구 입출력 스키마."""

from pydantic import BaseModel, Field


class EventListQuery(BaseModel):
    """일정 조회 요청."""

    time_min: str | None = Field(default=None, description="조회 시작 시간 (ISO 8601). 기본값: 현재 시간")
    time_max: str | None = Field(default=None, description="조회 종료 시간 (ISO 8601). 기본값: 오늘 끝")
    max_results: int = Field(default=10, description="최대 결과 수")


class EventCreate(BaseModel):
    """일정 생성 요청."""

    summary: str = Field(description="일정 제목")
    start_time: str = Field(description="시작 시간 (ISO 8601, e.g. 2025-01-15T14:00:00+09:00)")
    end_time: str = Field(description="종료 시간 (ISO 8601)")
    description: str = Field(default="", description="일정 설명")
    location: str = Field(default="", description="장소")


class EventUpdate(BaseModel):
    """일정 수정 요청."""

    event_id: str = Field(description="Google Calendar 이벤트 ID")
    summary: str | None = Field(default=None, description="변경할 제목")
    start_time: str | None = Field(default=None, description="변경할 시작 시간")
    end_time: str | None = Field(default=None, description="변경할 종료 시간")
    description: str | None = Field(default=None, description="변경할 설명")
    location: str | None = Field(default=None, description="변경할 장소")


class EventResponse(BaseModel):
    """일정 응답."""

    event_id: str
    summary: str
    start_time: str
    end_time: str
    description: str = ""
    location: str = ""
    html_link: str = ""
