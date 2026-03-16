# LangChain AI Assistant

A modular, command-line AI assistant built with Python and LangChain.
Developed for CIS 2777 – Project #2.

## Setup

### Prerequisites

- Python 3.10+
- A running LLM backend (e.g., [Ollama](https://ollama.com/) with `llama3`)

### Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd <repo-folder>

# Create and activate a virtual environment (recommended)
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS / Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Configuration

Model and API settings are centralized in `src/config.py`.  By default the
app connects to a local Ollama instance.  You can override settings with
environment variables:

| Variable      | Default                         | Description             |
|---------------|---------------------------------|-------------------------|
| `MODEL_NAME`  | `llama3`                        | Model identifier        |
| `BASE_URL`    | `http://localhost:11434/v1`     | API base URL            |
| `API_KEY`     | `ollama`                        | API key (Ollama ignores)|
| `TEMPERATURE` | `0.7`                           | Sampling temperature    |
| `MAX_TOKENS`  | `512`                           | Max response tokens     |

## Usage

All commands are run from the **project root** directory.

### 1. Templated Chain

Generates a beginner-friendly explanation of a topic.

```bash
python -m src.main template --topic "machine learning"
```

### 2. Structured Output

Produces a validated JSON analysis of a subject.

```bash
python -m src.main structured --input "photosynthesis"
```

### 3. Basic Chat

Interactive multi-turn chat (no memory between turns).

```bash
python -m src.main chat
```

### 4. Chat with Memory

Chat with a study coach that remembers your name, goals, and context.

```bash
python -m src.main memory-chat
```

### 5. Tool Chat

Chat where the model can invoke tools (word counter & math evaluator).

```bash
python -m src.main tool-chat
```

## Running Tests

```bash
pytest tests/ -v
```

Tests cover non-LLM logic: tool execution, output validation, and tool-call parsing.

## Project Structure

```
project-root/
├── README.md
├── requirements.txt
├── src/
│   ├── __init__.py
│   ├── main.py          # CLI dispatcher (argparse)
│   ├── config.py         # Centralized configuration
│   ├── chains/
│   │   ├── __init__.py
│   │   ├── template_chain.py    # Feature 1: Templated chain
│   │   └── structured_chain.py  # Feature 2: Structured output
│   ├── chat/
│   │   ├── __init__.py
│   │   ├── basic_chat.py        # Feature 3: Basic chat loop
│   │   └── memory_chat.py       # Feature 4: Chat with memory
│   └── tools/
│       ├── __init__.py
│       └── tool_chat.py         # Feature 5: Tool-based interaction
├── tests/
│   ├── __init__.py
│   ├── test_tools.py            # Tool function tests
│   ├── test_validation.py       # Structured output validation tests
│   └── test_parsing.py          # Tool-call parsing tests
└── screenshots/
    └── (screenshots of each feature)
```
