import subprocess
import threading


def execute_command(
    command: str,
    description: str,
    on_output=None,
) -> str:
    """Execute a shell command and stream its output."""

    output_lines = []

    try:
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
        )

        def kill_process():
            if process.poll() is None:
                process.kill()

        timer = threading.Timer(60, kill_process)
        timer.start()

        try:
            if process.stdout is not None:
                for line in process.stdout:
                    line = line.rstrip("\n")

                    output_lines.append(line)

                    if on_output:
                        on_output(line)

            return_code = process.wait()

        finally:
            timer.cancel()

        output = "\n".join(output_lines)

        return (
            f"{output}\n"
            f"Exit code: {return_code}"
        )

    except Exception as e:
        return f"Error executing command: {e}"


EXECUTE_COMMAND_TOOL = {
    "type": "function",
    "function": {
        "name": "execute_command",
        "description": (
            "Execute a shell command in the user's current project "
            "directory. Use this for running programs, tests, builds, "
            "git commands, and other terminal operations."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "command": {
                    "type": "string",
                    "description": "The shell command to execute.",
                },
                "description": {
                    "type": "string",
                    "description": (
                        "A short, clear explanation of what the command "
                        "will do. This is shown to the user before "
                        "they approve execution."
                    ),
                },
            },
            "required": [
                "command",
                "description",
            ],
        },
    },
}