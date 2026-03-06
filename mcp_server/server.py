"""FastMCP 서버 - Google Calendar 도구를 MCP 프로토콜로 노출."""

import sys
from pathlib import Path

# 프로젝트 루트를 sys.path에 추가 (standalone 실행 시)
_project_root = str(Path(__file__).resolve().parent.parent)
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

from mcp.server.fastmcp import FastMCP

from mcp_server.calendar_tools import (
    create_event,
    delete_event,
    list_events,
    update_event,
)
from mcp_server.models import (
    EventCreate,
    EventListQuery,
    EventResponse,
    EventUpdate,
)

mcp = FastMCP("Google Calendar Assistant")


@mcp.tool()
def calendar_list_events(req: EventListQuery) -> list[EventResponse]:
    """Google Calendar 일정을 조회합니다."""
    return list_events(req.time_min, req.time_max, req.max_results)


@mcp.tool()
def calendar_create_event(req: EventCreate) -> EventResponse:
    """Google Calendar에 새 일정을 생성합니다."""
    return create_event(req.summary, req.start_time, req.end_time, req.description, req.location)


@mcp.tool()
def calendar_update_event(req: EventUpdate) -> EventResponse:
    """기존 Google Calendar 일정을 수정합니다."""
    return update_event(req.event_id, req.summary, req.start_time, req.end_time, req.description, req.location)


@mcp.tool()
def calendar_delete_event(event_id: str) -> dict:
    """Google Calendar 일정을 삭제합니다."""
    return delete_event(event_id)


if __name__ == "__main__":
    mcp.run()
