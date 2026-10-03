from  qna import ask_gemini




def explain_concept(topic: str, level: str = "beginner") -> str:

    prompt = f"""
You are EduGenie, an AI educational tutor.

Explain this topic clearly:

Topic: {topic}
Student level: {level}

Include:
1. Simple definition
2. Step-by-step explanation
3. Important concepts
4. Simple example
5. Real-world application
6. Common mistakes
7. Key points to remember

Use language appropriate for the student's level.
"""

    return ask_gemini(prompt)
