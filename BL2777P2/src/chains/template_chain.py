"""
Templated Chain – Feature 1
===========================
Implements a prompt-based chain using PromptTemplate and StrOutputParser.
Accepts a topic from the command line and generates a concise explanation.
"""

from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

from src.config import MODEL_NAME, BASE_URL, API_KEY, TEMPERATURE, MAX_TOKENS


# ── Prompt Template (original – not copied from tutorials) ──────────────
_TEMPLATE = (
    "You are a knowledgeable tutor.  Given the topic below, provide a "
    "brief, beginner-friendly explanation in 3–5 sentences.  Focus on "
    "why the topic matters and give one real-world example.\n\n"
    "Topic: {topic}\n\n"
    "Explanation:"
)

prompt = PromptTemplate(
    input_variables=["topic"],
    template=_TEMPLATE,
)


def run_template_chain(topic: str) -> None:
    """Build and invoke the templated chain, then print the result."""

    llm = ChatOpenAI(
        model=MODEL_NAME,
        base_url=BASE_URL,
        api_key=API_KEY,
        temperature=TEMPERATURE,
        max_tokens=MAX_TOKENS,
    )

    # Chain:  prompt → model → string output parser
    chain = prompt | llm | StrOutputParser()

    print(f"\n Topic: {topic}")
    print("-" * 50)

    result: str = chain.invoke({"topic": topic})
    print(result.strip())
    print()
