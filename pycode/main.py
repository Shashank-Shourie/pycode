from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.live import Live
from prompt_toolkit import PromptSession
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.formatted_text import HTML
from rich.text import Text
from rich.box import ROUNDED

from pycode.agent import Agent

from pycode.utils.diff import build_edit_diff

console = Console()


class ResponseRenderer:
    """
    Streams assistant text into a live-updating Panel.

    While tokens are arriving, the panel shows plain text (fast, no
    flicker). The instant the stream stops -- either because the turn
    finished or because a tool call is about to interrupt it -- the
    same panel is redrawn once as rendered Markdown, so the final
    result looks clean.
    """

    def __init__(self, console: Console):
        self.console = console
        self.buffer = ""
        self.live: Live | None = None

    def _panel(self, final: bool = False) -> Panel:
        body = Markdown(self.buffer) if final else self.buffer
        return Panel(
            body,
            title="Pycode",
            border_style="green",
        )

    def add_chunk(self, chunk: str):
        if self.live is None:
            self.buffer = ""
            self.live = Live(
                self._panel(),
                console=self.console,
                refresh_per_second=16,
                vertical_overflow="visible",
            )
            self.live.start()

        self.buffer += chunk
        self.live.update(self._panel())

    def finalize(self):
        """Stop the live panel and leave a nicely formatted version behind."""
        if self.live is None:
            return

        if self.buffer.strip():
            self.live.update(self._panel(final=True))

        self.live.stop()
        self.live = None


renderer = ResponseRenderer(console)


def show_response_chunk(chunk: str):
    renderer.add_chunk(chunk)


def show_tool_output(line: str):
    renderer.finalize()
    console.print(
        f"[dim]|[/dim] {line}",
    )


def request_tool_permission(tool_name: str, arguments: dict) -> bool:
    renderer.finalize()

    if tool_name == "execute_command":
        description = arguments["description"]
        details = f"$ {arguments['command']}"
    elif tool_name == "write_file":
        description = f"Write file '{arguments['path']}'"
        details = arguments["path"]
    elif tool_name == "edit_file":
        description = f"Edit file '{arguments['path']}'"
        details = build_edit_diff(arguments)
    else:
        description = f"Execute tool '{tool_name}'"
        details = str(arguments)

    panel_content = Text()
    panel_content.append(description, style="bold",)
    panel_content.append("\n\n")


    if isinstance(details,Text):
        panel_content.append(details)
    else:
        panel_content.append(str(details))

    console.print()
    console.print(
        Panel(
            panel_content,
            box=ROUNDED,
            title="Permission requested",
            border_style="yellow",
        )
    )

    answer = console.input(
        "[bold yellow]Allow? (y/N): [/bold yellow]"
    )

    return answer.strip() in ("y", "yes")


def show_welcome():
    console.print(
        Panel(
            "[bold]Pycode[/bold]\n"
            "AI Coding Assistant\n\n"
            "[dim]Type /help for commands[/dim]",
            box=ROUNDED,
            title="Welcome",
            border_style="blue",
        )
    )


def show_tool_call(tool_name: str, arguments: dict):
    renderer.finalize()

    console.print(
        f"\n[dim]-> Tool:[/dim] [cyan]{tool_name}[/cyan]"
    )

    console.print(
        f"[dim] Arguments:[/dim] {arguments}"
    )


def main():
    show_welcome()
    agent = Agent()

    history = InMemoryHistory()

    session = PromptSession(
        history=history
    )

    while True:
        try:
            user_input = session.prompt(
                HTML("\n<ansibrightblue>You &gt;</ansibrightblue> ")
            ).strip()

        except (KeyboardInterrupt, EOFError):
            console.print("\n[dim]Goodbye.[/dim]")
            break

        if not user_input:
            continue

        if user_input == "/exit" or user_input == "/quit":
            console.print("[dim]Goodbye.[/dim]")
            break

        if user_input == "/clear":
            agent.clear()
            console.clear()
            show_welcome()
            console.print("[dim]Conversation cleared.[/dim]")
            continue

        if user_input == "/help":
            console.print(
                Panel(
                    "[bold cyan]/clear[/bold cyan] Clear conversation\n"
                    "[green]/help[/green]  Show this help message\n"
                    "[red]/exit[/red]  Exit PyCode\n"
                    "[red]/quit[/red]  Exit PyCode",
                    box=ROUNDED,
                    title="Commands",
                    border_style="yellow",
                )
            )
            continue

        try:
            agent.run(
                user_input,
                on_tool_call=show_tool_call,
                request_permission=request_tool_permission,
                on_tool_output=show_tool_output,
                on_response_chunk=show_response_chunk
            )

            renderer.finalize()

        except Exception as e:
            renderer.finalize()
            console.print_exception()
            # console.print(
            #     Panel(
            #         str(e),
            #         box=ROUNDED,
            #         title="Error",
            #         border_style="red",
            #     )
            # )


if __name__ == "__main__":
    main()