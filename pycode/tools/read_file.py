from pathlib import Path


def read_file(path: str) -> str:
    """Read the contents of a file."""

    file_path = Path(path)

    if not file_path.exists():
        return f"Error: file '{path}' does not exist."

    if not file_path.is_file():
        return f"Error: '{path}' is not a file."

    try:
        return file_path.read_text()
    except Exception as e:
        return f"Error reading '{path}': {e}"


READ_FILE_TOOL = {
    "type": "function",
    "function": {
        "name": "read_file",
        "description": "Read the contents of a file.",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "The path of the file to read.",
                }
            },
            "required": ["path"],
        },
    },
}