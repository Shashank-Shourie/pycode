from pathlib import Path

def list_directory(path: str = ".") -> str:
    """List the contents of the directory"""

    directory = Path(path)

    if not directory.exists():
        return f"Error: directory '{path}' does not exist."

    if not directory.is_dir():
        return f"Error: directory '{path}' is not a directory"

    try:
        entries = sorted(directory.iterdir(), key=lambda p: (p.is_file(), p.name.lower()))

        if not entries:
            return f"Directory {path} is empty"

        result = []

        for entry in entries:
            if entry.is_dir():
                result.append(f"[DIR]  {entry.name}")
            else:
                result.append(f"[FILE] {entry.name}")

        return "\n".join(result)
    except Exception as e:
        return f"Error listing directory '{path}': {e}"

LIST_DIRECTORY_TOOL = {
    "type": "function",
    "function":{
        "name": "list_directory",
        "description": "List the files and directories inside a directory.",
        "parameters":{
            "type": "object",
            "properties":{
                "path":{
                    "type":"string",
                    "description": "Path of the directory to list. Defaults to the current directory.",
                }
            },
            "required":[],
        }
    }
}