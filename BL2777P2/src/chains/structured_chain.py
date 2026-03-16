"""
Structured Output Chain – Feature 2
====================================
Produces JSON-structured output and validates it against expected fields.
Given user input, the model returns a JSON object with defined keys.
"""

import json
from typing import Any

from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

from src.config import MODEL_NAME, BASE_URL, API_KEY, TEMPERATURE, MAX_TOKENS


# ── Prompt Template ─────────────────────────────────────────────────────
_TEMPLATE = (
    "You are an expert analyst.  Given the subject below, return ONLY a "
    "valid JSON object (no markdown, no extra text) with exactly these keys:\n\n"
    '  "subject"    – the subject echoed back as a string\n'
    '  "summary"    – a 1–2 sentence summary\n'
    '  "key_points" – a JSON array of exactly 3 short bullet-point strings\n'
    '  "difficulty" – one of "beginner", "intermediate", or "advanced"\n\n'
    "Subject: {input}\n\n"
    "JSON:"
)

prompt = PromptTemplate(
    input_variables=["input"],
    template=_TEMPLATE,
)

# ── Required fields and allowed values for validation ───────────────────
REQUIRED_FIELDS: list[str] = ["subject", "summary", "key_points", "difficulty"]
ALLOWED_DIFFICULTIES: set[str] = {"beginner", "intermediate", "advanced"}


def validate_structured_output(data: dict[str, Any]) -> list[str]:
    """Return a list of validation error messages (empty = valid)."""
    errors: list[str] = []

    # Check required fields exist
    for field in REQUIRED_FIELDS:
        if field not in data:
            errors.append(f"Missing required field: '{field}'")

    # Validate key_points is a list of exactly 3 items
    kp = data.get("key_points")
    if kp is not None:
        if not isinstance(kp, list):
            errors.append("'key_points' must be a JSON array")
        elif len(kp) != 3:
            errors.append(f"'key_points' must have exactly 3 items (got {len(kp)})")

    # Validate difficulty value
    diff = data.get("difficulty")
    if diff is not None and diff not in ALLOWED_DIFFICULTIES:
        errors.append(
            f"'difficulty' must be one of {ALLOWED_DIFFICULTIES} (got '{diff}')"
        )

    return errors


def run_structured_chain(user_input: str) -> None:
    """Build and invoke the structured chain, validate, and print results."""

    llm = ChatOpenAI(
        model=MODEL_NAME,
        base_url=BASE_URL,
        api_key=API_KEY,
        temperature=TEMPERATURE,
        max_tokens=MAX_TOKENS,
    )

    chain = prompt | llm | StrOutputParser()

    print(f"\n🔍 Input: {user_input}")
    print("-" * 50)

    raw: str = chain.invoke({"input": user_input})

    # Strip potential markdown code fences the model might add
    cleaned = raw.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.split("\n", 1)[-1]
    if cleaned.endswith("```"):
        cleaned = cleaned.rsplit("```", 1)[0]
    cleaned = cleaned.strip()

    # Attempt JSON parsing
    try:
        data: dict[str, Any] = json.loads(cleaned)
    except json.JSONDecodeError as exc:
        # Try to fix incomplete JSON by adding missing closing braces
        if not cleaned.endswith("}"):
            # Count opening and closing braces
            open_braces = cleaned.count("{")
            close_braces = cleaned.count("}")
            if open_braces > close_braces:
                # Add missing closing braces
                cleaned += "}" * (open_braces - close_braces)
                try:
                    data = json.loads(cleaned)
                    print("  Fixed incomplete JSON (added missing closing braces)")
                except json.JSONDecodeError:
                    print(f" JSON parsing failed: {exc}")
                    print(f"Raw output:\n{raw}")
                    return
            else:
                print(f" JSON parsing failed: {exc}")
                print(f"Raw output:\n{raw}")
                return
        else:
            print(f" JSON parsing failed: {exc}")
            print(f"Raw output:\n{raw}")
            return

    # Validate structure
    errors = validate_structured_output(data)
    if errors:
        print("  Validation issues:")
        for err in errors:
            print(f"   - {err}")
    else:
        print(" Validation passed!")

    # Pretty-print the JSON
    print("\nStructured Output:")
    print(json.dumps(data, indent=2))
    print()
