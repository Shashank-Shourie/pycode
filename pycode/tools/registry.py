from pycode.tools.read_file import read_file, READ_FILE_TOOL
from pycode.tools.list_directory import list_directory, LIST_DIRECTORY_TOOL
from pycode.tools.write_file import write_file, WRITE_FILE_TOOL
from pycode.tools.edit_file import edit_file, EDIT_FILE_TOOL
from pycode.tools.execute_command import execute_command, EXECUTE_COMMAND_TOOL


TOOLS = {
    "read_file": read_file,
    "list_directory": list_directory,
    "write_file": write_file,
    "edit_file": edit_file,
    "execute_command": execute_command
}


TOOL_DEFINITIONS = [
    READ_FILE_TOOL,
    LIST_DIRECTORY_TOOL,
    WRITE_FILE_TOOL,
    EDIT_FILE_TOOL,
    EXECUTE_COMMAND_TOOL
]