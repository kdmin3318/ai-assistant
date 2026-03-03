"""Rich 기반 CLI 출력 포맷터."""

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

console = Console()


def print_welcome():
    """환영 메시지를 출력한다."""
    console.print(
        Panel(
            "[bold cyan]AI 일정 관리 비서[/bold cyan]\n"
            "한국어로 일정을 관리하세요.\n"
            "[dim]종료: quit | exit | q[/dim]",
            border_style="cyan",
        )
    )


def print_assistant(message: str):
    """어시스턴트 메시지를 출력한다."""
    console.print(f"\n[bold green]🤖 비서:[/bold green] {message}")


def print_user_prompt() -> str:
    """사용자 입력 프롬프트를 출력하고 입력을 받는다."""
    console.print()
    return console.input("[bold blue]👤 나:[/bold blue] ")


def print_error(message: str):
    """에러 메시지를 출력한다."""
    console.print(f"\n[bold red]❌ 오류:[/bold red] {message}")


def print_info(message: str):
    """정보 메시지를 출력한다."""
    console.print(f"\n[dim]ℹ️  {message}[/dim]")


def print_events_table(events: list[dict]):
    """일정 목록을 테이블로 출력한다."""
    if not events:
        print_assistant("조회된 일정이 없습니다.")
        return

    table = Table(title="📅 일정 목록", border_style="cyan")
    table.add_column("시간", style="cyan", width=20)
    table.add_column("제목", style="bold")
    table.add_column("장소", style="dim")

    for event in events:
        start = event.get("start_time", "")
        # ISO 8601에서 보기 좋게 변환
        if "T" in start:
            start = start.split("T")[0] + " " + start.split("T")[1][:5]
        table.add_row(
            start,
            event.get("summary", ""),
            event.get("location", ""),
        )

    console.print()
    console.print(table)


def print_confirmation(message: str) -> bool:
    """확인 메시지를 출력하고 Y/N 응답을 받는다."""
    print_assistant(message)
    response = console.input("\n[bold yellow]👉 (Y/N):[/bold yellow] ").strip().lower()
    return response in ("y", "yes", "ㅛ", "네", "응")
