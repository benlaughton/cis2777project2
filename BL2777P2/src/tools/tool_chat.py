"""
Tool-Based Interaction – Feature 5
====================================
Implements two meaningfully different tools and a chat loop where the
model decides which tool to call based on the user's request.

Tools
-----
1. word_count  – counts the number of words in a given text string
2. math_eval   – safely evaluates a basic arithmetic expression
"""

import re
from typing import Any

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser

from src.config import (
    MODEL_NAME, BASE_URL, API_KEY,
    TEMPERATURE, MAX_TOKENS, EXIT_COMMANDS,
)

# ═══════════════════════════════════════════════════════════════════════════
# Tool definitions (plain Python functions)
# ═══════════════════════════════════════════════════════════════════════════

def word_count(text: str) -> dict[str, Any]:
    """Count the number of words in the supplied text."""
    words = text.split()
    return {"tool": "word_count", "input": text, "count": len(words)}


def math_eval(expression: str) -> dict[str, Any]:
    """Safely evaluate a basic arithmetic expression (+, -, *, /, **)."""
    # Allow only digits, whitespace, and basic operators
    if not re.match(r'^[\d\s\+\-\*\/\.\(\)]+$', expression):
        return {"tool": "math_eval", "input": expression, "error": "Invalid expression"}
    try:
        result = eval(expression)  # safe because we validated the input
        return {"tool": "math_eval", "input": expression, "result": result}
    except Exception as exc:
        return {"tool": "math_eval", "input": expression, "error": str(exc)}


# Registry so we can look tools up by name
TOOLS: dict[str, Any] = {
    "word_count": word_count,
    "math_eval": math_eval,
}


# ═══════════════════════════════════════════════════════════════════════════
# Parsing helper – extract tool name and argument from model output
# ═══════════════════════════════════════════════════════════════════════════

def parse_tool_call(model_output: str) -> tuple[str | None, str | None]:
    """
    Expect the model to output a line like:
        TOOL: tool_name | ARGUMENT: some argument text

    Returns (tool_name, argument) or (None, None) if parsing fails.
    """
    match = re.search(
        r'TOOL:\s*(\w+)\s*\|\s*ARGUMENT:\s*(.+)',
        model_output,
        re.IGNORECASE,
    )
    if match:
        return match.group(1).strip().lower(), match.group(2).strip()
    return None, None


# ═══════════════════════════════════════════════════════════════════════════
# Chat loop
# ═══════════════════════════════════════════════════════════════════════════

_SYSTEM_PROMPT = (
    "You are a helpful assistant with access to two tools.\n\n"
    "Available tools:\n"
    "  word_count – counts words in a piece of text\n"
    "  math_eval  – evaluates a basic arithmetic expression\n\n"
    "When the user asks you to use a tool, respond with EXACTLY this format "
    "(on a single line, no extra text):\n"
    "TOOL: <tool_name> | ARGUMENT: <argument>\n\n"
    "Examples:\n"
    "  TOOL: word_count | ARGUMENT: The quick brown fox\n"
    "  TOOL: math_eval | ARGUMENT: 42 * 7 + 3\n\n"
    "If the user is just chatting and does NOT need a tool, reply normally "
    "WITHOUT the TOOL:/ARGUMENT: format."
)


def run_tool_chat() -> None:
    """Interactive loop where the model decides which tool to invoke."""

    llm = ChatOpenAI(
        model=MODEL_NAME,
        base_url=BASE_URL,
        api_key=API_KEY,
        temperature=TEMPERATURE,
        max_tokens=MAX_TOKENS,
    )

    system_msg = SystemMessage(content=_SYSTEM_PROMPT)

    print("\n  Tool Chat")
    print("Ask me to count words or do math!")
    print(f"Type one of {EXIT_COMMANDS} to quit.\n")

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if not user_input:
            continue
        if user_input.lower() in EXIT_COMMANDS:
            print("Goodbye!")
            break

        messages = [system_msg, HumanMessage(content=user_input)]
        response = llm.invoke(messages)
        raw_output: str = response.content

        # Try to parse a tool call from the model's response
        tool_name, argument = parse_tool_call(raw_output)

        if tool_name and argument:
            if tool_name in TOOLS:
                result = TOOLS[tool_name](argument)
                print(f"  [Tool called: {tool_name}]")
                print(f"  Result: {result}\n")
            else:
                print(f"    Unknown tool '{tool_name}'. Available: {list(TOOLS.keys())}\n")
        else:
            # Model chose to answer directly
            print(f"Assistant: {raw_output}\n")
