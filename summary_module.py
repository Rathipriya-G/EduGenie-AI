from ai_service import generate_text
from config import get_settings
from demo_service import demo_summary
from prompts import SUMMARY_PROMPT


def summarize_text(text: str) -> str:
    settings = get_settings()

    # Use Demo Mode when Gemini is unavailable
    if settings.demo_mode:
        return demo_summary(text)

    # Normal Gemini mode
    prompt = SUMMARY_PROMPT.format(text=text)

    return generate_text(prompt)