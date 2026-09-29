from ai_service import generate_text
from config import get_settings
from demo_service import demo_qa
from prompts import QA_PROMPT


def answer_question(text: str) -> str:
    settings = get_settings()

    if settings.demo_mode:
        return demo_qa(text)

    prompt = QA_PROMPT.format(text=text)
    return generate_text(prompt)