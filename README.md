# pycode

A simple AI coding agent built in Python — a "Claude Code" equivalent built from scratch. `pycode` runs as a CLI tool powered by the Groq API.

## Features

- Command-line AI coding agent
- Powered by [Groq](https://groq.com/) for fast LLM inference
- Clean terminal output via [Rich](https://github.com/Textualize/rich)

## Prerequisites

- Python 3.11 or higher
- A [Groq API key](https://console.groq.com/keys) (free to create — sign up on the Groq console)

## Installation

Clone the repository:

```bash
git clone https://github.com/Shashank-Shourie/pycode.git
cd pycode
```

Install the project (this uses the `pyproject.toml` and pulls in `groq`, `rich`, and `python-dotenv`):

```bash
pip install -e .
```

## Setup: Add your Groq API key

`pycode` needs a Groq API key to talk to the model. Create a `.env` file in the project root:

```bash
touch .env
```

Add your key to it:

```
GROQ_API_KEY=your_groq_api_key_here
```

Get a free API key from the [Groq Console](https://console.groq.com/keys) if you don't already have one.

## Usage

Once installed and your API key is set, run:

```bash
pycode "<Your Prompt>"
```

This launches the CLI entry point defined in `pyproject.toml` (`pycode.main:main`).
## Project structure

```
pycode/
├── pycode/           # Main package source
├── tests/            # Test suite
├── pyproject.toml    # Project metadata & dependencies
└── .env              # Your local Groq API key (not committed)
```

## Running tests

If you have `pytest` installed:

```bash
pytest tests/
```

## License

No license specified yet — add one (e.g. MIT) if you plan to share this publicly.
