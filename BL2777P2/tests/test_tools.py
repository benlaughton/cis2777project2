"""
Tests for tool execution logic (word_count, math_eval).
These test the non-LLM Python functions directly.
"""

import pytest
from src.tools.tool_chat import word_count, math_eval


class TestWordCount:
    """Tests for the word_count tool."""

    def test_basic_sentence(self) -> None:
        result = word_count("The quick brown fox")
        assert result["count"] == 4
        assert result["tool"] == "word_count"

    def test_single_word(self) -> None:
        result = word_count("hello")
        assert result["count"] == 1

    def test_empty_string(self) -> None:
        result = word_count("")
        assert result["count"] == 0

    def test_extra_whitespace(self) -> None:
        result = word_count("  hello   world  ")
        assert result["count"] == 2

    def test_input_preserved(self) -> None:
        text = "testing input preservation"
        result = word_count(text)
        assert result["input"] == text


class TestMathEval:
    """Tests for the math_eval tool."""

    def test_addition(self) -> None:
        result = math_eval("2 + 3")
        assert result["result"] == 5

    def test_multiplication(self) -> None:
        result = math_eval("6 * 7")
        assert result["result"] == 42

    def test_complex_expression(self) -> None:
        result = math_eval("(10 + 5) * 2")
        assert result["result"] == 30

    def test_division(self) -> None:
        result = math_eval("100 / 4")
        assert result["result"] == 25.0

    def test_exponentiation(self) -> None:
        result = math_eval("2 ** 8")
        assert result["result"] == 256

    def test_invalid_expression_letters(self) -> None:
        result = math_eval("abc + 1")
        assert "error" in result

    def test_invalid_expression_commands(self) -> None:
        result = math_eval("import os")
        assert "error" in result

    def test_tool_name(self) -> None:
        result = math_eval("1 + 1")
        assert result["tool"] == "math_eval"
