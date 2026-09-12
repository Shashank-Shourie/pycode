from pathlib import Path
import difflib

from rich.text import Text


def build_edit_diff(arguments: dict) -> Text:
    """Generate a colored unified diff for a proposed edit."""

    path = arguments["path"]
    old_text = arguments["old_text"]
    new_text = arguments["new_text"]

    file_path = Path(path)

    if not file_path.exists():
        return Text("Error: file does not exist.", style="red")

    if not file_path.is_file():
        return Text("Error: path is not a file.", style="red")

    try:
        current_content = file_path.read_text()

        occurrences = current_content.count(old_text)

        if occurrences == 0:
            return Text(
                "Error: the specified text was not found "
                "in the current file.",
                style="red",
            )

        if occurrences > 1:
            return Text(
                f"Error: the specified text occurs {occurrences} "
                "times in the current file.",
                style="red",
            )

        updated_content = current_content.replace(
            old_text,
            new_text,
            1,
        )

        diff = difflib.unified_diff(
            current_content.splitlines(),
            updated_content.splitlines(),
            fromfile=f"a/{path}",
            tofile=f"b/{path}",
        )

        result = Text()

        for line in diff:
            if line.startswith("+") and not line.startswith("+++"):
                result.append(line + "\n", style="green")

            elif line.startswith("-") and not line.startswith("---"):
                result.append(line + "\n", style="red")

            else:
                result.append(line + "\n")

        return result

    except Exception as e:
        return Text(
            f"Error generating diff: {e}",
            style="red",
        )