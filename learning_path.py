from ai_service import generate_structured
from config import get_settings
from prompts import LEARNING_PATH_PROMPT
from schemas import LearningPathResponse


def get_learning_recommendations(text: str) -> LearningPathResponse:
    settings = get_settings()

    # Use Demo Mode when Gemini is unavailable
    if settings.demo_mode:
        from demo_service import demo_learning_path
        return demo_learning_path(text)

    # Normal Gemini mode
    prompt = LEARNING_PATH_PROMPT.format(text=text)

    result = generate_structured(
        prompt,
        LearningPathResponse,
    )

    # Validate exactly 3 learning stages
    if len(result.steps) != 3:
        raise ValueError(
            "Learning path must contain exactly 3 stages."
        )

    expected_levels = [
        "Beginner",
        "Intermediate",
        "Advanced",
    ]

    actual_levels = [
        step.level
        for step in result.steps
    ]

    if actual_levels != expected_levels:
        raise ValueError(
            "Learning path must contain Beginner, Intermediate, and Advanced stages in order."
        )

    return result