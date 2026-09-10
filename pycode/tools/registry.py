from pycode.tools.tool import Tool

from pycode.tools.read_file import read_file, READ_FILE_TOOL
from pycode.tools.list_directory import list_directory, LIST_DIRECTORY_TOOL
from pycode.tools.write_file import write_file, WRITE_FILE_TOOL
from pycode.tools.edit_file import edit_file, EDIT_FILE_TOOL
from pycode.tools.execute_command import execute_command, EXECUTE_COMMAND_TOOL


TOOLS = {
    "read_file": Tool(
        name="read_file",
        function=read_file,
        definition=READ_FILE_TOOL,
        requires_permission=False,
        supports_streaming=False,
    ),

    "list_directory": Tool(
        name="list_directory",
        function=list_directory,
        definition=LIST_DIRECTORY_TOOL,
        requires_permission=False,
        supports_streaming=False,
    ),

    "write_file": Tool(
        name="write_file",
        function=write_file,
        definition=WRITE_FILE_TOOL,
        requires_permission=False,
        supports_streaming=False,
    ),

    "edit_file": Tool(
        name="edit_file",
        function=edit_file,
        definition=EDIT_FILE_TOOL,
        requires_permission=False,
        supports_streaming=False,
    ),

    "execute_command": Tool(
        name="execute_command",
        function=execute_command,
        definition=EXECUTE_COMMAND_TOOL,
        requires_permission=True,
        supports_streaming=True,
    ),
}

TOOL_DEFINITIONS = [
    tool.definition
    for tool in TOOLS.values()
]