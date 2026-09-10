from pathlib import Path

def write_file(path: str, content: str) -> str:
    """Create or overwrite a file with the provided content."""

    file_path = Path(path)

    try:
        file_path.write_text(content)

        return f"Successfully wrote to '{path}'."
    except Exception as e:
        return f"Error writing to '{path}': {e}"

WRITE_FILE_TOOL = {
    "type": "function",
    "function":{
        "name":"write_file",
        "description":"Create a new file or overwrite an existing file with the provided content.",
        "parameters":{
            "type":"object",
            "properties":{
                "path":{
                    "type":"string",
                    "description":"Path of the file to create or overwrite.",
                },
                "content":{
                    "type":"string",
                    "description":"Complete contents that should be wriiten to the file.",
                },
            },
            "required":["path","content"],
        },
    },
}