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
            "GEMINI_API_KEY is not configured. "
            "Add it to your .env file."
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
    """
    Return True for temporary Gemini availability/server errors.
    """

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
    ]

    return any(code in message for code in retryable_codes)


def generate_text(prompt: str) -> str:
    settings = get_settings()
    client = get_client()

    max_attempts = 4

    for attempt in range(max_attempts):
        try:
            from google.genai import types

            response = client.models.generate_content(
                model=settings.gemini_model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=settings.gemini_temperature,
                    max_output_tokens=settings.gemini_max_output_tokens,
                ),
            )

            text = getattr(response, "text", None)

            if not text:
                raise AIServiceError(
                    "Gemini returned an empty response."
                )

            return text.strip()

        except AIServiceError:
            raise

        except Exception as exc:

            if _is_retryable_error(exc):

                if attempt < max_attempts - 1:
                    wait_seconds = 2 ** attempt

                    print(
                        f"Gemini temporarily unavailable. "
                        f"Retrying in {wait_seconds} seconds..."
                    )

                    time.sleep(wait_seconds)
                    continue

                raise AIServiceError(
                    "Gemini is temporarily unavailable after "
                    f"{max_attempts} attempts. "
                    "Please try again later."
                ) from exc

            raise AIServiceError(
                f"Gemini request failed: {exc}"
            ) from exc


def generate_structured(
    prompt: str,
    response_model: type[T],
) -> T:

    settings = get_settings()
    client = get_client()

    max_attempts = 4

    for attempt in range(max_attempts):

        try:
            from google.genai import types

            response = client.models.generate_content(
                model=settings.gemini_model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=settings.gemini_temperature,
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

            return response_model.model_validate_json(text)

        except AIServiceError:
            raise

        except Exception as exc:

            if _is_retryable_error(exc):

                if attempt < max_attempts - 1:
                    wait_seconds = 2 ** attempt

                    print(
                        f"Gemini temporarily unavailable. "
                        f"Retrying in {wait_seconds} seconds..."
                    )

                    time.sleep(wait_seconds)
                    continue

                raise AIServiceError(
                    "Gemini is temporarily unavailable after "
                    f"{max_attempts} attempts. "
                    "Please try again later."
                ) from exc

            raise AIServiceError(
                f"Structured Gemini request failed: {exc}"
            ) from exc