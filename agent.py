import os
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

from tools import (
    analyze_structure,
    compute_complexity,
    check_documentation,
    security_scan,
    rag_retrieve,
)

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.2,
    api_key=os.getenv("GROQ_API_KEY")
)

REVIEW_PROMPT = ChatPromptTemplate.from_template("""
You are CodeSentinel, an expert Python code reviewer.

Analyze the following results and produce a professional report.

## Structure Analysis
{structure}

## Complexity Analysis
{complexity}

## Documentation Analysis
{documentation}

## Security Analysis
{security}

## Best Practices Retrieved
{best_practices}

## Source Code
{code}

Generate:

1. Executive Summary
2. Metrics Table
3. Findings
4. Recommendations
5. Final Verdict
""")

def review_code(code: str):

    structure = analyze_structure.invoke(code)

    complexity = compute_complexity.invoke(code)

    documentation = check_documentation.invoke(code)

    security = security_scan.invoke(code)

    rag_results = []

    if "Missing docstrings" in documentation:
        rag_results.append(
            rag_retrieve.invoke("python docstring best practices")
        )

    if "Cyclomatic complexity" in complexity:
        rag_results.append(
            rag_retrieve.invoke("reduce cyclomatic complexity")
        )

    if "unsafe" in security.lower():
        rag_results.append(
            rag_retrieve.invoke("python security best practices")
        )

    best_practices = "\n\n".join(rag_results)

    chain = REVIEW_PROMPT | llm

    response = chain.invoke({
        "structure": structure,
        "complexity": complexity,
        "documentation": documentation,
        "security": security,
        "best_practices": best_practices,
        "code": code
    })

    return response.content