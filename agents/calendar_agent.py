"""Calendar Agent - MCP 클라이언트로 Google Calendar 도구 호출."""

import asyncio
import json
import sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from agents.base import BaseAgent


class CalendarAgent(BaseAgent):
    """MCP 서버를 통해 Google Calendar를 조작하는 에이전트."""

    def __init__(self):
        super().__init__("CalendarAgent")
        self._server_script = str(
            Path(__file__).resolve().parent.parent / "mcp_server" / "server.py"
        )

    async def process(self, user_input: str) -> dict:
        """직접 호출되지 않음. call_tool을 사용."""
        return {"error": "Use call_tool() instead"}

    async def call_tool(self, tool_name: str, arguments: dict) -> dict:
        """MCP 서버의 도구를 호출한다.

        Args:
            tool_name: 호출할 도구 이름 (calendar_list_events 등)
            arguments: 도구에 전달할 인자
        """
        server_params = StdioServerParameters(
            command=sys.executable,
            args=[self._server_script],
        )

        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()

                result = await session.call_tool(tool_name, arguments)

                # MCP 응답에서 텍스트 콘텐츠 추출
                if result.content:
                    for item in result.content:
                        if hasattr(item, "text"):
                            return json.loads(item.text)
                return {"error": "No response from MCP server"}

    async def list_events(
        self,
        time_min: str | None = None,
        time_max: str | None = None,
        max_results: int = 10,
    ) -> list[dict] | dict:
        """일정 목록을 조회한다."""
        args = {"max_results": max_results}
        if time_min:
            args["time_min"] = time_min
        if time_max:
            args["time_max"] = time_max
        return await self.call_tool("calendar_list_events", args)

    async def create_event(
        self,
        summary: str,
        start_time: str,
        end_time: str,
        description: str = "",
        location: str = "",
    ) -> dict:
        """새 일정을 생성한다."""
        return await self.call_tool(
            "calendar_create_event",
            {
                "summary": summary,
                "start_time": start_time,
                "end_time": end_time,
                "description": description,
                "location": location,
            },
        )

    async def update_event(
        self,
        event_id: str,
        summary: str | None = None,
        start_time: str | None = None,
        end_time: str | None = None,
        description: str | None = None,
        location: str | None = None,
    ) -> dict:
        """기존 일정을 수정한다."""
        args = {"event_id": event_id}
        if summary is not None:
            args["summary"] = summary
        if start_time is not None:
            args["start_time"] = start_time
        if end_time is not None:
            args["end_time"] = end_time
        if description is not None:
            args["description"] = description
        if location is not None:
            args["location"] = location
        return await self.call_tool("calendar_update_event", args)

    async def delete_event(self, event_id: str) -> dict:
        """일정을 삭제한다."""
        return await self.call_tool("calendar_delete_event", {"event_id": event_id})
