"""Google Calendar MCP 도구들."""

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from googleapiclient.discovery import build

from config.settings import settings
from mcp_server.auth import get_google_credentials


def _get_calendar_service():
    """Google Calendar API 서비스 객체를 반환한다."""
    creds = get_google_credentials(
        settings.google_credentials_path,
        settings.google_token_path,
    )
    return build("calendar", "v3", credentials=creds)


def list_events(
    time_min: str | None = None,
    time_max: str | None = None,
    max_results: int = 10,
) -> list[dict]:
    """일정 목록을 조회한다.

    Args:
        time_min: 조회 시작 시간 (ISO 8601). 기본값: 현재 시간
        time_max: 조회 종료 시간 (ISO 8601). 기본값: 오늘 끝
        max_results: 최대 결과 수
    """
    service = _get_calendar_service()
    tz = ZoneInfo(settings.timezone)
    now = datetime.now(tz)

    if not time_min:
        time_min = now.isoformat()
    if not time_max:
        end_of_day = now.replace(hour=23, minute=59, second=59)
        time_max = end_of_day.isoformat()

    result = (
        service.events()
        .list(
            calendarId=settings.google_calendar_id,
            timeMin=time_min,
            timeMax=time_max,
            maxResults=max_results,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )

    events = []
    for event in result.get("items", []):
        start = event["start"].get("dateTime", event["start"].get("date"))
        end = event["end"].get("dateTime", event["end"].get("date"))
        events.append({
            "event_id": event["id"],
            "summary": event.get("summary", "(제목 없음)"),
            "start_time": start,
            "end_time": end,
            "description": event.get("description", ""),
            "location": event.get("location", ""),
            "html_link": event.get("htmlLink", ""),
        })
    return events


def create_event(
    summary: str,
    start_time: str,
    end_time: str,
    description: str = "",
    location: str = "",
) -> dict:
    """새 일정을 생성한다.

    Args:
        summary: 일정 제목
        start_time: 시작 시간 (ISO 8601)
        end_time: 종료 시간 (ISO 8601)
        description: 일정 설명
        location: 장소
    """
    service = _get_calendar_service()

    event_body = {
        "summary": summary,
        "description": description,
        "location": location,
        "start": {"dateTime": start_time, "timeZone": settings.timezone},
        "end": {"dateTime": end_time, "timeZone": settings.timezone},
    }

    event = (
        service.events()
        .insert(calendarId=settings.google_calendar_id, body=event_body)
        .execute()
    )

    return {
        "event_id": event["id"],
        "summary": event.get("summary", ""),
        "start_time": event["start"].get("dateTime", ""),
        "end_time": event["end"].get("dateTime", ""),
        "description": event.get("description", ""),
        "location": event.get("location", ""),
        "html_link": event.get("htmlLink", ""),
    }


def update_event(
    event_id: str,
    summary: str | None = None,
    start_time: str | None = None,
    end_time: str | None = None,
    description: str | None = None,
    location: str | None = None,
) -> dict:
    """기존 일정을 수정한다.

    Args:
        event_id: 수정할 이벤트 ID
        summary: 변경할 제목
        start_time: 변경할 시작 시간
        end_time: 변경할 종료 시간
        description: 변경할 설명
        location: 변경할 장소
    """
    service = _get_calendar_service()

    event = (
        service.events()
        .get(calendarId=settings.google_calendar_id, eventId=event_id)
        .execute()
    )

    if summary is not None:
        event["summary"] = summary
    if start_time is not None:
        event["start"] = {"dateTime": start_time, "timeZone": settings.timezone}
    if end_time is not None:
        event["end"] = {"dateTime": end_time, "timeZone": settings.timezone}
    if description is not None:
        event["description"] = description
    if location is not None:
        event["location"] = location

    updated = (
        service.events()
        .update(
            calendarId=settings.google_calendar_id,
            eventId=event_id,
            body=event,
        )
        .execute()
    )

    return {
        "event_id": updated["id"],
        "summary": updated.get("summary", ""),
        "start_time": updated["start"].get("dateTime", ""),
        "end_time": updated["end"].get("dateTime", ""),
        "description": updated.get("description", ""),
        "location": updated.get("location", ""),
        "html_link": updated.get("htmlLink", ""),
    }


def delete_event(event_id: str) -> dict:
    """일정을 삭제한다.

    Args:
        event_id: 삭제할 이벤트 ID
    """
    service = _get_calendar_service()

    service.events().delete(
        calendarId=settings.google_calendar_id,
        eventId=event_id,
    ).execute()

    return {"event_id": event_id, "deleted": True}
