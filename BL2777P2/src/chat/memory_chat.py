"""
Chat with Memory – Feature 4
==============================
Multi-turn chat that uses LangChain memory utilities so the model
remembers earlier parts of the conversation.

Uses RunnableWithMessageHistory and InMemoryChatMessageHistory as
required by the project specification.
"""

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

from src.config import (
    MODEL_NAME, BASE_URL, API_KEY,
    TEMPERATURE, MAX_TOKENS,
    MEMORY_SYSTEM_PROMPT, SESSION_ID, EXIT_COMMANDS,
)


def run_memory_chat() -> None:
    """Run a chat loop with conversational memory."""

    llm = ChatOpenAI(
        model=MODEL_NAME,
        base_url=BASE_URL,
        api_key=API_KEY,
        temperature=TEMPERATURE,
        max_tokens=MAX_TOKENS,
    )

    # Prompt includes a placeholder that will be filled with chat history
    prompt = ChatPromptTemplate.from_messages([
        ("system", MEMORY_SYSTEM_PROMPT),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}"),
    ])

    chain = prompt | llm

    # In-memory store keyed by session id
    store: dict[str, InMemoryChatMessageHistory] = {}

    def get_session_history(session_id: str) -> InMemoryChatMessageHistory:
        if session_id not in store:
            store[session_id] = InMemoryChatMessageHistory()
        return store[session_id]

    # Wrap the chain with message history support
    chain_with_memory = RunnableWithMessageHistory(
        chain,
        get_session_history,
        input_messages_key="input",
        history_messages_key="history",
    )

    config = {"configurable": {"session_id": SESSION_ID}}

    print("\n Chat with Memory (study coach)")
    print("Tell me your name and what you're studying – I'll remember!")
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

        response = chain_with_memory.invoke({"input": user_input}, config=config)
        print(f"Coach: {response.content}\n")
