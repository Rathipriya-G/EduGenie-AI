from typing import Literal

from pydantic import BaseModel, Field, field_validator


# =========================================================
# Generic text request
# =========================================================

class TextRequest(BaseModel):

    text: str = Field(
        ...,
        min_length=2,
        max_length=30000,
    )

    @field_validator("text")
    @classmethod
    def normalize_text(
        cls,
        value: str,
    ) -> str:

        value = value.strip()

        if len(value) < 2:

            raise ValueError(
                "Please provide at least 2 characters."
            )

        return value


# =========================================================
# Quiz
# =========================================================

class QuizOption(BaseModel):

    id: Literal[
        "A",
        "B",
        "C",
        "D",
    ]

    text: str


class QuizQuestion(BaseModel):

    question: str

    options: list[QuizOption] = Field(
        min_length=4,
        max_length=4,
    )

    correct_answer: Literal[
        "A",
        "B",
        "C",
        "D",
    ]

    explanation: str


class QuizResponse(BaseModel):

    title: str

    questions: list[QuizQuestion] = Field(
        min_length=3,
        max_length=3,
    )


# =========================================================
# Learning Path
# =========================================================

class LearningStep(BaseModel):

    level: Literal[
        "Beginner",
        "Intermediate",
        "Advanced",
    ]

    topics: list[str]

    suggested_time: str

    resources: list[str]


class LearningPathResponse(BaseModel):

    topic: str

    goal: str

    steps: list[LearningStep] = Field(
        min_length=3,
        max_length=3,
    )


# =========================================================
# Generic response
# =========================================================

class TextResponse(BaseModel):

    result: str


# =========================================================
# Health
# =========================================================

class HealthResponse(BaseModel):

    status: str

    gemini_configured: bool

    model: str