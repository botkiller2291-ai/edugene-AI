import json
import re

from  qna import ask_gemini


def generate_quiz(
    topic: str,
    number_of_questions: int = 3,
    difficulty: str = "medium",
):
    """
    Generate a quiz and always return a list of question objects.

    Each question contains:
    - question
    - options (exactly 4)
    - answer
    - explanation
    """

    prompt = f"""
You are EduGenie, an educational quiz generator.

Create a quiz about: {topic}

Requirements:
- Generate exactly {number_of_questions} questions.
- Difficulty: {difficulty}.
- Every question must have exactly 4 options.
- There must be exactly 1 correct answer.
- The "answer" must exactly match one of the options.
- Include a short explanation.
- Return ONLY valid JSON.
- Do NOT use Markdown.
- Do NOT use ```json.

Return exactly this format:

{{
    "questions": [
        {{
            "question": "Question text",
            "options": [
                "Option A",
                "Option B",
                "Option C",
                "Option D"
            ],
            "answer": "Option B",
            "explanation": "Short explanation."
        }}
    ]
}}
"""

    result = ask_gemini(prompt)

    if not result:
        raise RuntimeError("Gemini returned an empty quiz response.")

    # Remove accidental Markdown code fences.
    cleaned = result.strip()
    cleaned = re.sub(r"^```json\s*", "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"^```\s*", "", cleaned)
    cleaned = re.sub(r"\s*```$", "", cleaned)

    try:
        data = json.loads(cleaned)
    except json.JSONDecodeError as exc:
        raise RuntimeError(
            f"Gemini returned invalid quiz JSON: {exc}"
        ) from exc

    # Accept either:
    # {"questions": [...]}
    # or directly [...]
    if isinstance(data, dict):
        questions = data.get("questions")
    elif isinstance(data, list):
        questions = data
    else:
        questions = None

    if not isinstance(questions, list):
        raise RuntimeError(
            "Quiz response does not contain a valid questions array."
        )

    validated_questions = []

    for index, item in enumerate(questions):
        if not isinstance(item, dict):
            raise RuntimeError(
                f"Quiz question {index + 1} is not a valid object."
            )

        question = str(item.get("question", "")).strip()
        options = item.get("options")
        answer = str(item.get("answer", "")).strip()
        explanation = str(item.get("explanation", "")).strip()

        if not question:
            raise RuntimeError(
                f"Quiz question {index + 1} has no question text."
            )

        if not isinstance(options, list) or len(options) != 4:
            raise RuntimeError(
                f"Quiz question {index + 1} must have exactly 4 options."
            )

        options = [str(option).strip() for option in options]

        if any(not option for option in options):
            raise RuntimeError(
                f"Quiz question {index + 1} contains an empty option."
            )

        if answer not in options:
            raise RuntimeError(
                f"Quiz question {index + 1} has an answer "
                f"that does not match any option."
            )

        validated_questions.append(
            {
                "question": question,
                "options": options,
                "answer": answer,
                "explanation": explanation,
            }
        )

    if not validated_questions:
        raise RuntimeError("Gemini returned no quiz questions.")

    # Return ONLY the array because main.py wraps it as:
    # {"questions": generate_quiz(...)}
    return validated_questions
