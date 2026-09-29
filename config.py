import os
from functools import lru_cache

from dotenv import load_dotenv
from pydantic import BaseModel, Field, field_validator


load_dotenv()


class Settings(BaseModel):

    gemini_api_key: str = Field(
        default="",
        validation_alias="GEMINI_API_KEY",
    )

    gemini_model: str = Field(
        default="gemini-3.8-flash",
        validation_alias="GEMINI_MODEL",
    )

    gemini_temperature: float = Field(
        default=0.4,
        validation_alias="GEMINI_TEMPERATURE",
    )

    gemini_max_output_tokens: int = Field(
        default=2048,
        validation_alias="GEMINI_MAX_OUTPUT_TOKENS",
    )

    use_local_explainer: bool = Field(
        default=False,
        validation_alias="USE_LOCAL_EXPLAINER",
    )

    demo_mode: bool = Field(
    default=False,
    validation_alias="DEMO_MODE"
    )

    local_explainer_model: str = Field(
        default="MBZUAI/LaMini-Flan-T5-783M",
        validation_alias="LOCAL_EXPLAINER_MODEL",
    )

    host: str = Field(
        default="127.0.0.1",
        validation_alias="HOST",
    )

    port: int = Field(
        default=8000,
        validation_alias="PORT",
    )

    @field_validator("gemini_temperature")
    @classmethod
    def validate_temperature(
        cls,
        value: float,
    ) -> float:

        if not 0 <= value <= 2:

            raise ValueError(
                "GEMINI_TEMPERATURE must be between 0 and 2"
            )

        return value

    @field_validator("gemini_max_output_tokens")
    @classmethod
    def validate_tokens(
        cls,
        value: int,
    ) -> int:

        if value < 128:

            raise ValueError(
                "GEMINI_MAX_OUTPUT_TOKENS must be at least 128"
            )

        return value


@lru_cache
def get_settings() -> Settings:

    return Settings(

        GEMINI_API_KEY=os.getenv(
            "GEMINI_API_KEY",
            "",
        ),

        GEMINI_MODEL=os.getenv(
            "GEMINI_MODEL",
            "gemini-3.8-flash",
        ),

        GEMINI_TEMPERATURE=float(
            os.getenv(
                "GEMINI_TEMPERATURE",
                "0.4",
            )
        ),

        GEMINI_MAX_OUTPUT_TOKENS=int(
            os.getenv(
                "GEMINI_MAX_OUTPUT_TOKENS",
                "2048",
            )
        ),

        USE_LOCAL_EXPLAINER=(
            os.getenv(
                "USE_LOCAL_EXPLAINER",
                "false",
            ).lower()
            == "true"
        ),
        DEMO_MODE=(os.getenv("DEMO_MODE", "false").lower() == "true"),
        LOCAL_EXPLAINER_MODEL=os.getenv(
            "LOCAL_EXPLAINER_MODEL",
            "MBZUAI/LaMini-Flan-T5-783M",
        ),

        HOST=os.getenv(
            "HOST",
            "127.0.0.1",
        ),

        PORT=int(
            os.getenv(
                "PORT",
                "8000",
            )
        ),
    )