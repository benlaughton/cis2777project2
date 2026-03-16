"""
Basic Chat Loop – Feature 3
============================
Multi-turn interactive chat with no memory persistence.
Each exchange is independent; the model does not recall prior turns.
"""

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

from src.config import (
    MODEL_NAME, BASE_URL, API_KEY,
    TEMPERATURE, MAX_TOKENS,
    CHAT_SYSTEM_PROMPT, EXIT_COMMANDS,
)


def run_basic_chat() -> None:
    """Run an interactive chat loop until the user exits."""

    llm = ChatOpenAI(
        model=MODEL_NAME,
        base_url=BASE_URL,
        api_key=API_KEY,
        temperature=TEMPERATURE,
        max_tokens=MAX_TOKENS,
    )

    system_msg = SystemMessage(content=CHAT_SYSTEM_PROMPT)

    print("\n Basic Chat (no memory)")
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

        # Each turn is a fresh list – no history carried over
        messages = [system_msg, HumanMessage(content=user_input)]
        response = llm.invoke(messages)

        print(f"Assistant: {response.content}\n")
