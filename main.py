from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from ai_service import AIServiceError
from config import get_settings
from explanation_module import explain_concept
from learning_path import get_learning_recommendations
from qna import answer_question
from quiz_module import generate_quiz
from schemas import (
    HealthResponse,
    LearningPathResponse,
    QuizResponse,
    TextRequest,
    TextResponse,
)
from summary_module import summarize_text


BASE_DIR = Path(__file__).resolve().parent


app = FastAPI(
    title="EduGenie API",
    description="Gemini-powered educational learning assistant.",
    version="1.0.0",
)


# ---------------------------------------------------------
# Static files
# ---------------------------------------------------------

app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "static"),
    name="static",
)


# ---------------------------------------------------------
# Templates
# ---------------------------------------------------------

templates = Jinja2Templates(
    directory=str(BASE_DIR / "templates")
)


# ---------------------------------------------------------
# AI Error Handler
# ---------------------------------------------------------

@app.exception_handler(AIServiceError)
async def ai_error_handler(
    request: Request,
    exc: AIServiceError,
):
    from fastapi.responses import JSONResponse

    return JSONResponse(
        status_code=502,
        content={
            "detail": str(exc)
        },
    )


# ---------------------------------------------------------
# Frontend
# ---------------------------------------------------------

@app.get(
    "/",
    response_class=HTMLResponse,
)
async def home(request: Request):

    return templates.TemplateResponse(
    request=request,
    name="index.html",
    context={},
)


# ---------------------------------------------------------
# Health Check
# ---------------------------------------------------------

@app.get(
    "/health",
    response_model=HealthResponse,
)
async def health():

    settings = get_settings()

    return HealthResponse(
        status="ok",
        gemini_configured=bool(
            settings.gemini_api_key
        ),
        model=settings.gemini_model,
    )


# =========================================================
# QUESTION ANSWERING
# =========================================================

@app.post(
    "/api/qa",
    response_model=TextResponse,
)
@app.post(
    "/qa",
    response_model=TextResponse,
    include_in_schema=False,
)
async def qa(
    payload: TextRequest,
):

    answer = answer_question(
        payload.text
    )

    return TextResponse(
        result=answer
    )


# =========================================================
# CONCEPT EXPLANATION
# =========================================================

@app.post(
    "/api/explain",
    response_model=TextResponse,
)
@app.post(
    "/explain",
    response_model=TextResponse,
    include_in_schema=False,
)
async def explain(
    payload: TextRequest,
):

    explanation = explain_concept(
        payload.text
    )

    return TextResponse(
        result=explanation
    )


# =========================================================
# QUIZ
# =========================================================

@app.post(
    "/api/quiz",
    response_model=QuizResponse,
)
@app.post(
    "/quiz",
    response_model=QuizResponse,
    include_in_schema=False,
)
async def quiz(
    payload: TextRequest,
):

    return generate_quiz(
        payload.text
    )


# =========================================================
# SUMMARIZATION
# =========================================================

@app.post(
    "/api/summarize",
    response_model=TextResponse,
)
@app.post(
    "/summarize",
    response_model=TextResponse,
    include_in_schema=False,
)
async def summarize(
    payload: TextRequest,
):

    summary = summarize_text(
        payload.text
    )

    return TextResponse(
        result=summary
    )


# =========================================================
# LEARNING PATH
# =========================================================

@app.post(
    "/api/learn/recommendations",
    response_model=LearningPathResponse,
)
@app.post(
    "/learn/recommendations",
    response_model=LearningPathResponse,
    include_in_schema=False,
)
async def learning_recommendations(
    payload: TextRequest,
):

    return get_learning_recommendations(
        payload.text
    )


# =========================================================
# Run directly with:
# python main.py
# =========================================================

if __name__ == "__main__":

    import uvicorn

    settings = get_settings()

    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=True,
    )