import json

from pycode.llm import ask_llm
from pycode.tools.registry import TOOLS, TOOL_DEFINITIONS

SYSTEM_PROMPT = """
You are PyCode, an AI coding assistant.

You can inspect files in the user's project using the available tools.

Use tools when they are necessary to answer the user's request.
Use read_file before making assumptions about the contents of a file.

Use list_directory when you need to understand the project structure.

Use edit_file for targeted changes to existing files.

Use write_file when creating a new file or intentionally replacing
an entire file.

Use execute_command when you need to run programs, tests, builds,
git commands, or other shell operations.

When requesting execute_command, provide a short and accurate
description explaining exactly what the command will do.

Do not claim that a command succeeded unless you actually executed it
and inspected its result.
"""

class Agent:
    def __init__(self):
        self.messages = [
            {
                "role" : "system",
                "content": SYSTEM_PROMPT,
            }
        ]

    def execute_tool(self, tool_name:str, arguments:dict) -> str:
        """Find and execute a registered tool."""

        tool = TOOLS.get(tool_name)

        if tool is None:
            return f"Error: unknown tool '{tool_name}'."

        try:
            return tool(**arguments)
        except Exception as e:
            return f"Error executing '{tool_name}': {e}"

    def run(self, user_prompt: str, on_tool_call=None, request_permission=None) -> str:
        """Process one user message while keeping conversation history."""

        self.messages.append(
            {
                "role":"user",
                "content":user_prompt
            }
        )

        while True:
            response = ask_llm(
                self.messages,
                tools=TOOL_DEFINITIONS,
            )

            message = response.choices[0].message

            if not message.tool_calls:
                self.messages.append(
                    {
                        "role":"assistant",
                        "content":message.content,
                    }
                )

                return message.content

            self.messages.append(
                {
                    "role":"assistant",
                    "content":message.content,
                    "tool_calls":[
                        {
                            "id": tool_call.id,
                            "type": "function",
                            "function": {
                                "name": tool_call.function.name,
                                "arguments": tool_call.function.arguments,
                            },
                        }
                        for tool_call in message.tool_calls
                    ],
                }
            )

            for tool_call in message.tool_calls:
                tool_name = tool_call.function.name

                arguments = json.loads(tool_call.function.arguments)

                if on_tool_call:
                    on_tool_call(tool_name,arguments)

                if tool_name == "execute_command":
                    if request_permission is None:
                        result = (
                            "Error: Commansd execution requires user permission."
                        )
                    else:
                        allowed = request_permission(
                            arguments["command"],
                            arguments["description"],
                        )

                        if allowed:
                            result = self.execute_tool(
                                tool_name,arguments
                            )
                        else:
                            result = (
                                "Command execution was rejected by the user."
                            )
                else:
                    result = self.execute_tool(tool_name,arguments)

                self.messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result
                })

    def clear(self):
        """Clear the conversation history."""

        self.messages = [
            {
                "role":"system",
                "content":SYSTEM_PROMPT,
            }
        ]