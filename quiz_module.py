from ai_service import generate_structured
from config import get_settings
from prompts import QUIZ_PROMPT
from schemas import QuizResponse


def generate_quiz(text: str) -> QuizResponse:
    settings = get_settings()

    # Use Demo Mode when Gemini is temporarily unavailable
    if settings.demo_mode:
        from demo_service import demo_quiz
        return demo_quiz(text)

    # Normal Gemini mode
    prompt = QUIZ_PROMPT.format(text=text)

    result = generate_structured(
        prompt,
        QuizResponse,
    )

    # Validate exactly 3 questions
    if len(result.questions) != 3:
        raise ValueError("Quiz must contain exactly 3 questions.")

    # Validate exactly 4 options per question
    for question in result.questions:
        if len(question.options) != 4:
            raise ValueError(
                "Each quiz question must contain exactly 4 options."
            )

    return result