"""CLI 채팅 루프 - 진입점."""

import asyncio
import sys
from pathlib import Path

# 프로젝트 루트를 sys.path에 추가
_project_root = str(Path(__file__).resolve().parent.parent)
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

from agents.orchestrator import Orchestrator
from cli.formatter import (
    print_welcome,
    print_assistant,
    print_user_prompt,
    print_error,
    print_info,
    print_events_table,
    print_confirmation,
)


async def chat_loop():
    """메인 채팅 루프."""
    orchestrator = Orchestrator()
    print_welcome()

    while True:
        try:
            user_input = print_user_prompt()
        except (EOFError, KeyboardInterrupt):
            print_info("종료합니다. 안녕히 가세요!")
            break

        text = user_input.strip()
        if not text:
            continue
        if text.lower() in ("quit", "exit", "q", "종료"):
            print_info("종료합니다. 안녕히 가세요!")
            break

        try:
            result = await orchestrator.process(text)
        except Exception as e:
            print_error(str(e))
            continue

        response_type = result.get("type", "chat")

        if response_type == "chat":
            print_assistant(result["message"])

        elif response_type == "list":
            data = result.get("data", {})
            events = data.get("events", [])
            if events:
                print_events_table(events)
            else:
                print_assistant(result["message"])

        elif response_type == "confirmation":
            confirmed = print_confirmation(result["message"])
            if confirmed:
                print_info("작업을 실행합니다...")
                try:
                    exec_result = await orchestrator.confirm_and_execute()
                    print_assistant(exec_result["message"])
                    # 생성/수정 결과에 이벤트 정보가 있으면 표시
                    event_data = exec_result.get("data", {}).get("event")
                    if event_data:
                        link = event_data.get("html_link", "")
                        if link:
                            print_info(f"캘린더 링크: {link}")
                except Exception as e:
                    print_error(f"작업 실행 실패: {e}")
            else:
                msg = orchestrator.cancel_pending()
                print_assistant(msg)

        else:
            print_assistant(result.get("message", ""))


def main():
    """CLI 진입점."""
    asyncio.run(chat_loop())


if __name__ == "__main__":
    main()
