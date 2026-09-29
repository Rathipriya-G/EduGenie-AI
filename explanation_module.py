from __future__ import annotations

from ai_service import (
    AIServiceError,
    generate_text,
)

from config import get_settings

from prompts import EXPLAIN_PROMPT


_local_pipeline = None


# =========================================================
# Local LaMini Model
# =========================================================

def _local_explain(
    text: str,
) -> str:

    global _local_pipeline

    try:

        from transformers import pipeline

    except ImportError as exc:

        raise AIServiceError(
            "Local explanation requires "
            "transformers, torch and sentencepiece."
        ) from exc

    if _local_pipeline is None:

        settings = get_settings()

        _local_pipeline = pipeline(

            "text2text-generation",

            model=settings.local_explainer_model,
        )

    prompt = (
        "Explain this concept to a beginner "
        "in simple language. "
        "Give a definition, intuition, "
        "example and takeaway: "
        + text
    )

    result = _local_pipeline(

        prompt,

        max_new_tokens=350,

        do_sample=False,
    )

    if not result:

        raise AIServiceError(
            "Local explanation model returned no result."
        )

    return result[0][
        "generated_text"
    ].strip()


# =========================================================
# Public Explanation Function
# =========================================================

def explain_concept(text: str) -> str:
    settings = get_settings()

    if settings.demo_mode:
        from demo_service import demo_explanation
        return demo_explanation(text)

    if settings.use_local_explainer:
        try:
            return _local_explain(text)
        except Exception as exc:
            print(f"Local explanation model failed: {exc}")
            print("Falling back to Gemini.")

    prompt = EXPLAIN_PROMPT.format(text=text)
    return generate_text(prompt)