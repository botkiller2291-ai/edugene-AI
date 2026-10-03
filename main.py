import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

# ---------------------------------------------------------
# Base directory
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent

# ---------------------------------------------------------
# Load .env
# ---------------------------------------------------------

load_dotenv(
    BASE_DIR / ".env",
    override=True,
)

# ---------------------------------------------------------
# Import EduGenie modules
# ---------------------------------------------------------

from explanation_module import explain_concept
from learning_path import recommend_learning_path
from qna import answer_question
from quiz_module import generate_quiz
from summary_module import summarize_text


# ---------------------------------------------------------
# FastAPI app
# ---------------------------------------------------------

app = FastAPI(
    title="EduGenie",
    description="AI-powered educational assistant",
    version="1.0.0",
)


# ---------------------------------------------------------
# Static files
# ---------------------------------------------------------

static_directory = BASE_DIR / "static"

if static_directory.exists():
    app.mount(
        "/static",
        StaticFiles(directory=static_directory),
        name="static",
    )


# ---------------------------------------------------------
# Templates
# ---------------------------------------------------------

templates = Jinja2Templates(
    directory=str(BASE_DIR / "templates")
)


# ---------------------------------------------------------
# Request models
# ---------------------------------------------------------

class QuestionIn(BaseModel):
    question: str = Field(
        min_length=3,
        max_length=5000,
    )


class TopicIn(BaseModel):
    topic: str = Field(
        min_length=2,
        max_length=500,
    )


class TextIn(BaseModel):
    text: str = Field(
        min_length=20,
        max_length=20000,
    )


# ---------------------------------------------------------
# Helper function
# ---------------------------------------------------------

def run_module(function, *args):
    try:
        return function(*args)

    except HTTPException:
        raise

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )


# ---------------------------------------------------------
# Home page
# ---------------------------------------------------------

@app.get("/", response_class=HTMLResponse)
def home(request: Request):

    index_file = BASE_DIR / "templates" / "index.html"

    if not index_file.exists():
        return HTMLResponse(
            content="""
            <html>
                <head>
                    <title>EduGenie</title>
                </head>
                <body>
                    <h1>EduGenie API is running</h1>
                    <p>Open <a href="/docs">/docs</a> to test the API.</p>
                </body>
            </html>
            """,
            status_code=200,
        )

    return templates.TemplateResponse(
        request=request,
        name="index.html",
    )


# ---------------------------------------------------------
# Health check
# ---------------------------------------------------------

@app.get("/health")
def health():

    return {
        "status": "ok",
        "gemini_model": os.getenv(
            "GEMINI_MODEL",
            "gemini-3.8-flash",
        ),
        "gemini_key_set": bool(
            os.getenv("GEMINI_API_KEY")
        ),
    }


# ---------------------------------------------------------
# Question Answering
# ---------------------------------------------------------

@app.post("/qa")
def qa(data: QuestionIn):

    return run_module(
        answer_question,
        data.question,
    )


# ---------------------------------------------------------
# Alternative question endpoint
# ---------------------------------------------------------

@app.post("/ask")
def ask(data: QuestionIn):

    return run_module(
        answer_question,
        data.question,
    )


# ---------------------------------------------------------
# Explain concept
# ---------------------------------------------------------

@app.post("/explain")
def explain(data: TopicIn):

    return run_module(
        explain_concept,
        data.topic,
    )


# ---------------------------------------------------------
# Learning path
# ---------------------------------------------------------

@app.post("/learning-path")
def learning_path(data: TopicIn):

    return run_module(
        recommend_learning_path,
        data.topic,
    )


# ---------------------------------------------------------
# Generate quiz
# ---------------------------------------------------------

@app.post("/quiz")
def quiz(data: TopicIn):

    return run_module(
        generate_quiz,
        data.topic,
    )


# ---------------------------------------------------------
# Summarize text
# ---------------------------------------------------------

@app.post("/summarize")
def summarize(data: TextIn):

    return run_module(
        summarize_text,
        data.text,
    )
