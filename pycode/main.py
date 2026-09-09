import json
import argparse

from rich.console import Console

from pycode.agent import run_agent

console = Console()

def main():

    parser = argparse.ArgumentParser(
        description="Pycode - AI Coding Agent"
    )

    parser.add_argument(
        "prompt",
        help="Instruction for the coding agent"
    )

    args = parser.parse_args()


    response = run_agent(args.prompt)

    console.print(response)


if __name__ == "__main__":
    main()