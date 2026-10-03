from  qna import ask_gemini


def recommend_learning_path(
    goal: str,
    current_level: str = "beginner"
) -> str:

    prompt = f"""
You are EduGenie, an AI learning-path planner.

Create a structured learning path.

Learning goal:
{goal}

Current level:
{current_level}

Include:

1. Prerequisites
2. Beginner topics
3. Intermediate topics
4. Advanced topics
5. Practice exercises
6. Mini projects
7. Final project

Put the topics in a logical learning order.
"""

    return ask_gemini(prompt)
