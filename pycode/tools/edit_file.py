from pathlib import Path

def edit_file(path:str, old_text: str, new_text:str) -> str:
    """Replace an exact piece of text in a file."""

    file_path = Path(path)

    if not file_path.exists():
        return f"Error: file '{path}' does not exist."

    if not file_path.is_file():
        return f"Error: '{path}' is not a file."

    try:
        content = file_path.read_text()

        occurences = content.count(old_text)

        if occurences == 0:
            return (
                f"Error: The specified text was not found in '{path}'."
            )

        if occurences > 1:
            return(
                f"Error: The specified text occurs {occurences} times "
                f"in '{path}'. It must occur exactly once."
            )

        updated_content = content.replace(old_text,new_text,1)

        file_path.write_text(updated_content)

        return f"Successfully edited '{path}'."
    except Exception as e:
        return f"Error editing '{path}': {e}"

EDIT_FILE_TOOL = {
    "type": "function",
    "function": {
        "name": "edit_file",
        "description":(
            "Edit an existing file by replacing one exact piece of text with new text. The old text must occur exactly once."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Path of the file to edit.",
                },
                "old_text": {
                    "type": "string",
                    "description": "Exact text to find in the file.",
                },
                "new_text": {
                    "type": "string",
                    "description": "Text that should replace the old text.",
                },
            },
            "required":[
                "path",
                "old_text",
                "new_text",
            ],
        },
    },
}