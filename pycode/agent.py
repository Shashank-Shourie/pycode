import json

from pycode.llm import ask_llm
from pycode.tools.registry import TOOLS, TOOL_DEFINITIONS


SYSTEM_PROMPT = """
You are PyCode, an AI coding assistant.

You can inspect and modify files in the user's project using the
available tools.

General rules:

- Understand the user's request before using tools.
- Use list_directory when you need to understand the project structure.
- Use read_file to inspect existing files before modifying them.
- Do not guess the contents of an existing file.
- Use edit_file for targeted changes to existing files.
- Use write_file when creating a new file or when intentionally
  replacing the entire contents of a file.
- Never use write_file to modify an existing file when edit_file can
  safely make the requested targeted change.
- After modifying a file, inspect or verify the result when necessary.
- Use execute_command to run programs, tests, builds, git commands,
  or other shell operations.
- When requesting execute_command, provide a short and accurate
  description explaining exactly what the command will do.
- Do not claim that a command or file modification succeeded unless
  you actually executed the tool and inspected its result.

File modification workflow:

1. Inspect the relevant files.
2. Understand the existing code.
3. Choose the smallest appropriate modification.
4. Use edit_file for targeted changes.
5. Use write_file only when creating a new file or replacing an
   entire file intentionally.
6. Verify the modification when appropriate.
"""


class Agent:

    MAX_ITERATIONS = 10

    def __init__(self):
        self.messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            }
        ]

    def execute_tool(
        self,
        tool_name: str,
        arguments: dict,
        on_output=None,
    ) -> str:

        tool = TOOLS.get(tool_name)

        if tool is None:
            return f"Error: unknown tool '{tool_name}'."

        try:

            if tool.supports_streaming:
                return tool.function(
                    **arguments,
                    on_output=on_output,
                )

            return tool.function(**arguments)

        except Exception as e:
            return f"Error executing '{tool_name}': {e}"

    def run(
        self,
        user_prompt: str,
        on_tool_call=None,
        request_permission=None,
        on_tool_output=None,
        on_response_chunk=None
    ) -> str:
        """Process one user message."""

        self.messages.append(
            {
                "role": "user",
                "content": user_prompt,
            }
        )

        for _ in range(self.MAX_ITERATIONS):

            response = ask_llm(
                self.messages,
                tools=TOOL_DEFINITIONS,
                stream=True
            )

            content = ""
            tool_calls = {}

            # --- Drain the whole stream first ---
            for chunk in response:
                if not chunk.choices:
                    continue

                delta = chunk.choices[0].delta

                if delta.content:
                    content += delta.content

                    if on_response_chunk:
                        on_response_chunk(delta.content)

                if delta.tool_calls:
                    for tool_call in delta.tool_calls:
                        index = tool_call.index

                        if index not in tool_calls:
                            tool_calls[index] = {
                                "id": "",
                                "name": "",
                                "arguments": "",
                            }
                        if tool_call.id:
                            tool_calls[index]["id"] = tool_call.id
                        if tool_call.function:
                            if tool_call.function.name:
                                tool_calls[index]["name"] = (
                                    tool_call.function.name
                                )
                            if tool_call.function.arguments:
                                tool_calls[index]["arguments"] += (
                                    tool_call.function.arguments
                                )

            # --- Now that the stream is fully consumed, decide what to do ---
            if not tool_calls:
                self.messages.append(
                    {
                        "role": "assistant",
                        "content": content,
                    }
                )
                return content

            assistant_tool_calls = []

            for tool_call in tool_calls.values():
                assistant_tool_calls.append(
                    {
                        "id": tool_call["id"],
                        "type": "function",
                        "function": {
                            "name": tool_call["name"],
                            "arguments": tool_call["arguments"],
                        },
                    }
                )

            self.messages.append(
                {
                    "role": "assistant",
                    "content": content or None,
                    "tool_calls": assistant_tool_calls,
                }
            )

            for tool_call in assistant_tool_calls:
                tool_name = tool_call["function"]["name"]

                try:
                    arguments = json.loads(
                        tool_call["function"]["arguments"]
                    )
                except json.JSONDecodeError as e:
                    result = f"Error: invalid tool arguments: {e}"

                    self.messages.append(
                        {
                            "role": "tool",
                            "tool_call_id": tool_call["id"],
                            "name": tool_name,
                            "content": result,
                        }
                    )

                    continue

                tool = TOOLS.get(tool_name)

                if tool is None:
                    result = f"Error: unknown tool '{tool_name}'."
                else:
                    if on_tool_call:
                        on_tool_call(
                            tool_name,
                            arguments,
                        )
                    if tool.requires_permission:
                        if request_permission is None:
                            result = (
                                "Error: This tool requires user permission."
                            )
                        else:
                            allowed = request_permission(
                                tool_name,
                                arguments,
                            )

                            if not allowed:
                                result = (
                                    "The user rejected this tool execution."
                                )
                            else:
                                result = self.execute_tool(
                                    tool_name, arguments, on_output=on_tool_output,
                                )
                    else:
                        result = self.execute_tool(
                            tool_name, arguments, on_output=on_tool_output
                        )

                self.messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call["id"],
                        "name": tool_name,
                        "content": str(result),
                    }
                )

        return (
            "Error: Maximum agent iterations reached. The agent may be in a tool-calling loop."
        )

    def clear(self):
        """Clear the conversation history."""

        self.messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            }
        ]