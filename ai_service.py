from __future__ import annotations

import time
from typing import TypeVar

from pydantic import BaseModel

from config import get_settings


T = TypeVar("T", bound=BaseModel)

_client = None


class AIServiceError(RuntimeError):
    pass


def get_client():
    global _client

    settings = get_settings()

    if not settings.gemini_api_key:
        raise AIServiceError(
            "GEMINI_API_KEY is not configured."
        )

    if _client is None:
        try:
            from google import genai

            _client = genai.Client(
                api_key=settings.gemini_api_key
            )

        except Exception as exc:
            raise AIServiceError(
                f"Could not initialize Gemini: {exc}"
            ) from exc

    return _client


def _is_retryable_error(exc: Exception) -> bool:
    message = str(exc).upper()

    retryable_codes = [
        "503",
        "UNAVAILABLE",
        "500",
        "INTERNAL",
        "502",
        "BAD_GATEWAY",
        "504",
        "DEADLINE_EXCEEDED",
        "429",
        "RESOURCE_EXHAUSTED",
    ]

    return any(code in message for code in retryable_codes)


def _get_models(settings):
    """
    Primary model is tried first.
    If it is temporarily unavailable, fallback models are tried.
    """

    models = [
        settings.gemini_model,
        "gemini-3.8-flash",
    
    ]

    # Remove duplicates while preserving order
    return list(dict.fromkeys(models))


def generate_text(prompt: str) -> str:

    settings = get_settings()
    client = get_client()

    models = _get_models(settings)

    last_error = None

    for model in models:

        for attempt in range(3):

            try:

                from google.genai import types

                response = client.models.generate_content(
                    model=model,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        max_output_tokens=settings.gemini_max_output_tokens,
                    ),
                )

                text = getattr(response, "text", None)

                if not text:
                    raise AIServiceError(
                        "Gemini returned an empty response."
                    )

                print(
                    f"Gemini request succeeded using model: {model}"
                )

                return text.strip()

            except AIServiceError:
                raise

            except Exception as exc:

                last_error = exc

                if _is_retryable_error(exc):

                    if attempt < 2:

                        wait_seconds = 2 ** attempt

                        print(
                            f"Gemini model {model} temporarily unavailable. "
                            f"Retrying in {wait_seconds} seconds..."
                        )

                        time.sleep(wait_seconds)

                        continue

                    print(
                        f"Model {model} unavailable after 3 attempts. "
                        "Trying fallback model..."
                    )

                    break

                raise AIServiceError(
                    f"Gemini request failed: {exc}"
                ) from exc

    raise AIServiceError(
        "Gemini is temporarily unavailable. "
        "EduGenie tried multiple Gemini models. "
        "Please try again shortly."
    ) from last_error


def generate_structured(
    prompt: str,
    response_model: type[T],
) -> T:

    settings = get_settings()
    client = get_client()

    models = _get_models(settings)

    last_error = None

    for model in models:

        for attempt in range(3):

            try:

                from google.genai import types

                response = client.models.generate_content(
                    model=model,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        max_output_tokens=settings.gemini_max_output_tokens,
                        response_mime_type="application/json",
                        response_schema=response_model,
                    ),
                )

                text = getattr(response, "text", None)

                if not text:
                    raise AIServiceError(
                        "Gemini returned an empty structured response."
                    )

                result = response_model.model_validate_json(text)

                print(
                    f"Structured Gemini request succeeded using model: {model}"
                )

                return result

            except AIServiceError:
                raise

            except Exception as exc:

                last_error = exc

                if _is_retryable_error(exc):

                    if attempt < 2:

                        wait_seconds = 2 ** attempt

                        print(
                            f"Gemini model {model} temporarily unavailable. "
                            f"Retrying in {wait_seconds} seconds..."
                        )

                        time.sleep(wait_seconds)

                        continue

                    print(
                        f"Model {model} unavailable after 3 attempts. "
                        "Trying fallback model..."
                    )

                    break

                raise AIServiceError(
                    f"Structured Gemini request failed: {exc}"
                ) from exc

    raise AIServiceError(
        "Gemini is temporarily unavailable. "
        "EduGenie tried multiple Gemini models. "
        "Please try again shortly."
    ) from last_error