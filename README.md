# EduGenie

AI-powered study companion.

| Endpoint | Module | Model |
|---|---|---|
| `POST /qa` | qna.py | Gemini 3.8 flash lite (API) |
| `POST /explain` | explanation_module.py | LaMini-Flan-T5-783M (local, CPU) |
| `POST /quiz` | quiz_module.py | Gemini 3.8 flash   |
| `POST /summarize` | summary_module.py | Gemini 3.8 flash  |
| `POST /learn/recommendations` | learning_path.py | Gemini 3.8 flash  |

## Run

```bash
pip install -r requirements.txt
export GEMINI_API_KEY="your-key"        # Windows: set GEMINI_API_KEY=your-key
# optional: export GEMINI_MODEL="gemini-1.5-pro"
uvicorn main:app --reload
```

Open http://127.0.0.1:8000 (API docs at /docs).
The LaMini model (~3 GB) downloads on the first `/explain` request.
