"""
Centralized configuration for the LangChain AI Assistant.

All model parameters, API settings, and application defaults are defined here
so they can be imported wherever needed instead of being hard-coded.
"""

import os

# ---------------------------------------------------------------------------
# Model / API Configuration
# ---------------------------------------------------------------------------
# By default we point at a local Ollama instance.  Override with env vars
# if you want to use OpenAI or another provider.
MODEL_NAME: str = os.getenv("MODEL_NAME", "llama3")
BASE_URL: str = os.getenv("BASE_URL", "http://localhost:11434/v1")
API_KEY: str = os.getenv("API_KEY", "ollama")  # Ollama ignores the key

# ---------------------------------------------------------------------------
# Generation Parameters
# ---------------------------------------------------------------------------
TEMPERATURE: float = float(os.getenv("TEMPERATURE", "0.7"))
MAX_TOKENS: int = int(os.getenv("MAX_TOKENS", "2048"))

# ---------------------------------------------------------------------------
# Chat Settings
# ---------------------------------------------------------------------------
EXIT_COMMANDS: list[str] = ["exit", "quit", "bye", "q"]
CHAT_SYSTEM_PROMPT: str = (
    "You are a helpful and friendly AI assistant. "
    "Answer questions clearly and concisely."
)

# ---------------------------------------------------------------------------
# Memory Chat Settings
# ---------------------------------------------------------------------------
MEMORY_SYSTEM_PROMPT: str = (
    "You are a personalized study coach. Remember all details the user "
    "shares about themselves (name, interests, goals) and reference that "
    "information in later responses to give tailored advice."
)
SESSION_ID: str = "default-session"
