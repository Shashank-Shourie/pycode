import os

from dotenv import load_dotenv
from groq import Groq

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise RuntimeError("GROQ_API_KEY is not set in .env")

client = Groq(
    api_key=api_key
)

MODEL = "openai/gpt-oss-20b"


def ask_llm(messages, tools=None, stream=False):
    """Send messages to the LLM"""
    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        tools=tools or [],
        tool_choice="auto",
        stream=stream
    )

    return response