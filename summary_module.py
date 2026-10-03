from  qna import ask_gemini


def summarize_text(text: str, level: str = "beginner") -> str:

    prompt = f"""
You are EduGenie, an AI study assistant.

Summarize this educational material:

{text}

Student level: {level}

Include:
- Main ideas
- Important concepts
- Important definitions
- Important formulas if present
- Key takeaways

Keep the summary clear and concise.
"""

    return ask_gemini(prompt)
