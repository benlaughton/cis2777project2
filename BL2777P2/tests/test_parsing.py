"""
Tests for the tool-call parsing logic used in the tool chat.
"""

import pytest
from src.tools.tool_chat import parse_tool_call


class TestParseToolCall:
    """Tests for parse_tool_call."""

    def test_valid_word_count_call(self) -> None:
        output = "TOOL: word_count | ARGUMENT: The quick brown fox"
        tool, arg = parse_tool_call(output)
        assert tool == "word_count"
        assert arg == "The quick brown fox"

    def test_valid_math_eval_call(self) -> None:
        output = "TOOL: math_eval | ARGUMENT: 42 * 7 + 3"
        tool, arg = parse_tool_call(output)
        assert tool == "math_eval"
        assert arg == "42 * 7 + 3"

    def test_case_insensitive(self) -> None:
        output = "tool: Math_Eval | argument: 1+1"
        tool, arg = parse_tool_call(output)
        assert tool == "math_eval"
        assert arg == "1+1"

    def test_no_tool_call(self) -> None:
        output = "I don't think I need a tool for that."
        tool, arg = parse_tool_call(output)
        assert tool is None
        assert arg is None

    def test_partial_format(self) -> None:
        output = "TOOL: word_count"
        tool, arg = parse_tool_call(output)
        assert tool is None  # missing ARGUMENT part

    def test_extra_whitespace(self) -> None:
        output = "TOOL:   word_count   |   ARGUMENT:   hello world  "
        tool, arg = parse_tool_call(output)
        assert tool == "word_count"
        assert arg == "hello world"
