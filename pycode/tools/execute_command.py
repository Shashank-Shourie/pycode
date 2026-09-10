import subprocess

def execute_command(command: str, description: str) -> str:
    """Execute a shell command and return its output."""

    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=60,
        )

        output = []

        if result.stdout:
            output.append(f"STDOUT:\n{result.stdout}")

        if result.stderr:
            output.append(f"STDERR:\n{result.stderr}")

        output.append(
            f"Exit code: {result.returncode}"
        )

        return "\n".join(output)
    except subprocess.TimeoutExpired:
        return "Error: Command timed out after 60 seconds."
    except Exception as e:
        return f"Error executing command: {e}"

EXECUTE_COMMAND_TOOL = {
    "type": "function",
    "function": {
        "name": "execute_command",
        "description": (
            "Execute a shell command in the user's current project directory. Use this for running programs, tests, build commands, git commands, and other terminal operations."
        ),
        "parameters":{
            "type":"object",
            "properties": {
                "command": {
                    "type":"string",
                    "description":"The shell command to execute.",
                },
                "description":{
                    "type":"string",
                    "description":(
                        "A short, clear explanation of what the command will do. This will be shown to the user before they approve execution."
                    ),
                },
            },
            "required":[
                "command",
                "description",
            ],
        },
    },
}