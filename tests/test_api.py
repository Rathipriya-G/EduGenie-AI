from unittest.mock import patch

from schemas import (
    LearningPathResponse,
    LearningStep,
    QuizOption,
    QuizQuestion,
    QuizResponse,
)


# =========================================================
# Home
# =========================================================

def test_home(client):

    response = client.get("/")

    assert response.status_code == 200

    assert "EduGenie" in response.text


# =========================================================
# Health
# =========================================================

def test_health(client):

    response = client.get(
        "/health"
    )

    assert response.status_code == 200

    assert response.json()["status"] == "ok"


# =========================================================
# Q&A
# =========================================================

@patch(
    "main.answer_question",
    return_value=(
        "The Pacific Ocean is "
        "the largest ocean."
    ),
)
def test_qa(
    mock_answer,
    client,
):

    response = client.post(

        "/api/qa",

        json={
            "text":
                "Which is the largest ocean?"
        },
    )

    assert response.status_code == 200

    assert response.json()[
        "result"
    ].startswith(
        "The Pacific"
    )

    mock_answer.assert_called_once()


# =========================================================
# Explanation
# =========================================================

@patch(
    "main.explain_concept",
    return_value="A simple explanation.",
)
def test_explain(
    mock_explain,
    client,
):

    response = client.post(

        "/api/explain",

        json={
            "text":
                "Explain gravity."
        },
    )

    assert response.status_code == 200

    assert response.json()[
        "result"
    ] == "A simple explanation."

    mock_explain.assert_called_once()


# =========================================================
# Quiz
# =========================================================

@patch(
    "main.generate_quiz",
    return_value=QuizResponse(

        title="Science Quiz",

        questions=[

            QuizQuestion(

                question=
                    "What revolves around the Sun?",

                options=[

                    QuizOption(
                        id="A",
                        text="Earth",
                    ),

                    QuizOption(
                        id="B",
                        text="Moon",
                    ),

                    QuizOption(
                        id="C",
                        text="Cloud",
                    ),

                    QuizOption(
                        id="D",
                        text="Atom",
                    ),
                ],

                correct_answer="A",

                explanation=
                    "Earth revolves around the Sun.",
            )

        ] * 3,
    ),
)
def test_quiz(
    mock_quiz,
    client,
):

    response = client.post(

        "/api/quiz",

        json={
            "text":
                "Earth revolves around the Sun."
        },
    )

    assert response.status_code == 200

    assert len(
        response.json()["questions"]
    ) == 3

    mock_quiz.assert_called_once()


# =========================================================
# Summary
# =========================================================

@patch(
    "main.summarize_text",
    return_value="A concise summary.",
)
def test_summary(
    mock_summary,
    client,
):

    response = client.post(

        "/api/summarize",

        json={
            "text":
                "A long educational passage."
        },
    )

    assert response.status_code == 200

    assert response.json()[
        "result"
    ] == "A concise summary."

    mock_summary.assert_called_once()


# =========================================================
# Learning Path
# =========================================================

@patch(
    "main.get_learning_recommendations",

    return_value=LearningPathResponse(

        topic="Python",

        goal=
            "Learn Python progressively.",

        steps=[

            LearningStep(

                level="Beginner",

                topics=[
                    "Syntax"
                ],

                suggested_time=
                    "1 week",

                resources=[
                    "Official documentation"
                ],
            ),

            LearningStep(

                level="Intermediate",

                topics=[
                    "Object-oriented programming"
                ],

                suggested_time=
                    "2 weeks",

                resources=[
                    "Practice projects"
                ],
            ),

            LearningStep(

                level="Advanced",

                topics=[
                    "Async programming"
                ],

                suggested_time=
                    "2 weeks",

                resources=[
                    "Advanced documentation"
                ],
            ),
        ],
    ),
)
def test_learning_path(
    mock_learning,
    client,
):

    response = client.post(

        "/api/learn/recommendations",

        json={
            "text":
                "Python"
        },
    )

    assert response.status_code == 200

    assert [
        x["level"]
        for x in response.json()["steps"]
    ] == [

        "Beginner",

        "Intermediate",

        "Advanced",
    ]

    mock_learning.assert_called_once()


# =========================================================
# Validation
# =========================================================

def test_validation(client):

    response = client.post(

        "/api/qa",

        json={
            "text": "x"
        },
    )

    assert response.status_code == 422