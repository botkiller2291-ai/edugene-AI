import os
import time
from pathlib import Path

from dotenv import load_dotenv
from google import genai


# ---------------------------------------------------------
# Load .env
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent

load_dotenv(
    BASE_DIR / ".env",
    override=True,
)


# ---------------------------------------------------------
# Gemini configuration
# ---------------------------------------------------------

DEFAULT_MODEL = "gemini-3.8-flash"

_client = None


# ---------------------------------------------------------
# Gemini client
# ---------------------------------------------------------

def get_client():
    global _client

    if _client is None:

        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise RuntimeError(
                "GEMINI_API_KEY is not set. "
                "Please add GEMINI_API_KEY to your .env file."
            )

        _client = genai.Client(
            api_key=api_key
        )

    return _client


# ---------------------------------------------------------
# Gemini request
# ---------------------------------------------------------

def ask_gemini(prompt: str) -> str:

    model = os.getenv(
        "GEMINI_MODEL",
        DEFAULT_MODEL,
    )

    max_retries = 5

    for attempt in range(max_retries):

        try:

            print(
                f"Sending request to Gemini "
                f"using {model}..."
            )

            response = get_client().models.generate_content(
                model=model,
                contents=prompt,
            )

            if not response.text:

                raise RuntimeError(
                    "Gemini returned an empty response."
                )

            print("Gemini response received.")

            return response.text.strip()

        except Exception as exc:

            error_text = str(exc)

            is_temporary_error = (
                "503" in error_text
                or "UNAVAILABLE" in error_text
                or "high demand" in error_text.lower()
                or "temporarily unavailable"
                in error_text.lower()
            )

            if is_temporary_error:

                if attempt < max_retries - 1:

                    wait_time = 2 ** attempt

                    print(
                        f"Gemini temporarily unavailable. "
                        f"Retry {attempt + 1}/{max_retries - 1} "
                        f"in {wait_time} seconds..."
                    )

                    time.sleep(wait_time)

                    continue

                raise RuntimeError(
                    "Gemini is temporarily busy. "
                    "Please try your question again "
                    "in a few seconds."
                ) from exc

            raise RuntimeError(
                f"Gemini API error using model "
                f"'{model}': {exc}"
            ) from exc

    raise RuntimeError(
        "Gemini is temporarily unavailable. "
        "Please try again."
    )


# ---------------------------------------------------------
# Question answering
# ---------------------------------------------------------

def answer_question(question: str) -> str:

    prompt = (
        "You are EduGenie, a friendly AI tutor.\n\n"

        "Answer the student's question clearly "
        "and accurately.\n"

        "Use simple language suitable for students.\n"

        "Give a short example when useful.\n"

        "Use headings or bullet points when they "
        "make the answer easier to understand.\n"

        "Do not unnecessarily make the answer complicated.\n\n"

        f"Student question:\n{question}"
    )

    return ask_gemini(prompt)
