from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from prompt_toolkit import PromptSession
from prompt_toolkit.history import InMemoryHistory

from pycode.agent import Agent

console = Console()

def show_tool_output(line: str):
    console.print(
        f"[dim]|[/dim] {line}",
    )

def request_command_permission(tool_name: str, arguments: dict) -> bool:
    command = arguments["command"]
    description = arguments["description"]

    console.print()
    console.print(
        Panel(
            f"[bold]{description}[/bold]\n\n"
            f"[yellow]$ {command}[/yellow]",
            title="Command execution requested",
            border_style="yellow",
        )
    )

    answer = console.input(
        "[bold yellow]Execute? (y/N): [/bold yellow]"
    )

    return answer.strip() in ("y","yes")

def show_welcome():
    console.print(
        Panel(
            "[bold]Pycode[/bold]\n"
            "AI Coding Assistant\n\n"
            "[dim]Type /help for commands[/dim]",
            title = "Welcome",
            border_style="blue",
        )
    )

def show_tool_call(tool_name: str, arguments: dict):
    console.print(
        f"\n[dim]-> Tool:[/dim] [cyan]{tool_name}[/cyan]"
    )

    console.print(
        f"[dim] Arguments:[/dim] {arguments}"
    )

def show_response(response:str):
    console.print(
        Panel(
            Markdown(response),
            title="Pycode",
            border_style="green",
        )
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
                "\nYou > "
            ).strip()

        except (KeyboardInterrupt,EOFError):
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
                    "/clear Clear conversation\n"
                    "/help  Show this jelp message\n"
                    "/exit  Exit PyCode\n"
                    "/quit  Exit PyCode",
                    title="Commands",
                    border_style="yellow",
                )
            )
            continue

        try:
            response = agent.run(
                user_input,
                on_tool_call=show_tool_call,
                request_permission=request_command_permission,
                on_tool_output=show_tool_output
            )

            show_response(response)

        except Exception as e:
            console.print(
                Panel(
                    str(e),
                    title="Error",
                    border_style="red",
                )
            )

if __name__ == "__main__":
    main()