"""
CLI Dispatcher – main.py
=========================
Single entry point for the application.  Uses argparse with subcommands
to route execution to the appropriate feature module.

Usage (from project root):
    python -m src.main template --topic "machine learning"
    python -m src.main structured --input "photosynthesis"
    python -m src.main chat
    python -m src.main memory-chat
    python -m src.main tool-chat
"""

import argparse

from src.chains.template_chain import run_template_chain
from src.chains.structured_chain import run_structured_chain
from src.chat.basic_chat import run_basic_chat
from src.chat.memory_chat import run_memory_chat
from src.tools.tool_chat import run_tool_chat


def main() -> None:
    parser = argparse.ArgumentParser(
        description="LangChain AI Assistant – a modular CLI tool"
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True,
        help="Select a mode of operation",
    )

    # ── 1. template ─────────────────────────────────────────────────────
    template_parser = subparsers.add_parser(
        "template",
        help="Run the templated chain on a topic",
    )
    template_parser.add_argument(
        "--topic",
        type=str,
        required=True,
        help="Topic to explain (e.g. 'blockchain')",
    )

    # ── 2. structured ───────────────────────────────────────────────────
    structured_parser = subparsers.add_parser(
        "structured",
        help="Generate structured JSON output for a subject",
    )
    structured_parser.add_argument(
        "--input",
        type=str,
        required=True,
        help="Subject to analyze (e.g. 'neural networks')",
    )

    # ── 3. chat ─────────────────────────────────────────────────────────
    subparsers.add_parser(
        "chat",
        help="Start a basic multi-turn chat (no memory)",
    )

    # ── 4. memory-chat ──────────────────────────────────────────────────
    subparsers.add_parser(
        "memory-chat",
        help="Start a chat with conversational memory",
    )

    # ── 5. tool-chat ────────────────────────────────────────────────────
    subparsers.add_parser(
        "tool-chat",
        help="Start a tool-based interaction chat",
    )

    # ── Dispatch ────────────────────────────────────────────────────────
    args = parser.parse_args()

    if args.command == "template":
        run_template_chain(args.topic)
    elif args.command == "structured":
        run_structured_chain(args.input)
    elif args.command == "chat":
        run_basic_chat()
    elif args.command == "memory-chat":
        run_memory_chat()
    elif args.command == "tool-chat":
        run_tool_chat()


if __name__ == "__main__":
    main()
