"""
Tests for structured output validation logic.
Verifies the validate_structured_output function without calling the LLM.
"""

import pytest
from src.chains.structured_chain import validate_structured_output


class TestValidateStructuredOutput:
    """Tests for the JSON validation function."""

    def test_valid_output(self) -> None:
        data = {
            "subject": "Python",
            "summary": "A popular programming language.",
            "key_points": ["Easy syntax", "Large ecosystem", "Versatile"],
            "difficulty": "beginner",
        }
        errors = validate_structured_output(data)
        assert errors == []

    def test_missing_field(self) -> None:
        data = {
            "subject": "Python",
            "summary": "A programming language.",
            "key_points": ["A", "B", "C"],
            # missing "difficulty"
        }
        errors = validate_structured_output(data)
        assert any("difficulty" in e for e in errors)

    def test_wrong_key_points_count(self) -> None:
        data = {
            "subject": "Python",
            "summary": "A programming language.",
            "key_points": ["A", "B"],
            "difficulty": "beginner",
        }
        errors = validate_structured_output(data)
        assert any("3 items" in e for e in errors)

    def test_key_points_not_list(self) -> None:
        data = {
            "subject": "Python",
            "summary": "A programming language.",
            "key_points": "not a list",
            "difficulty": "beginner",
        }
        errors = validate_structured_output(data)
        assert any("array" in e for e in errors)

    def test_invalid_difficulty(self) -> None:
        data = {
            "subject": "Python",
            "summary": "A programming language.",
            "key_points": ["A", "B", "C"],
            "difficulty": "expert",
        }
        errors = validate_structured_output(data)
        assert any("expert" in e for e in errors)

    def test_empty_dict(self) -> None:
        errors = validate_structured_output({})
        assert len(errors) == 4  # all four fields missing

    def test_all_difficulties_accepted(self) -> None:
        for level in ("beginner", "intermediate", "advanced"):
            data = {
                "subject": "X",
                "summary": "Y",
                "key_points": ["A", "B", "C"],
                "difficulty": level,
            }
            assert validate_structured_output(data) == []
