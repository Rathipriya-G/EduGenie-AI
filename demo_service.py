from __future__ import annotations

from quiz_module import QuizResponse
from schemas import LearningPathResponse


def demo_qa(text: str) -> str:
    return (
        f"Demo Answer\n\n"
        f"You asked: {text}\n\n"
        f"This is a demonstration response from EduGenie. "
        f"In normal mode, Gemini generates the educational answer. "
        f"Demo Mode is currently enabled because the Gemini service "
        f"is temporarily unavailable."
    )


def demo_explanation(text: str) -> str:
    return (
        f"Concept Explanation: {text}\n\n"
        f"Beginner-friendly explanation:\n"
        f"{text} is an important concept that can be understood by "
        f"breaking it into smaller ideas and learning them step by step.\n\n"
        f"Key points:\n"
        f"• Start with the basic definition.\n"
        f"• Understand the main components.\n"
        f"• Study a simple example.\n"
        f"• Practice using the concept.\n\n"
        f"This is a Demo Mode response. Gemini will provide the "
        f"full AI-generated explanation when the service is available."
    )


def demo_summary(text: str) -> str:
    return (
        f"Summary\n\n"
        f"The provided content is about: {text}\n\n"
        f"Main idea: The topic can be understood by identifying its "
        f"central concept, important points, and practical applications.\n\n"
        f"This is a Demo Mode summary. Gemini will generate a "
        f"content-specific summary when available."
    )


def demo_quiz(text: str) -> QuizResponse:
    return QuizResponse(
        title=f"Demo Quiz: {text}",
        questions=[
            {
                "question": f"What is the first step when learning {text}?",
                "options": [
                    {"id": "A", "text": "Understand the basic concept"},
                    {"id": "B", "text": "Skip the fundamentals"},
                    {"id": "C", "text": "Avoid examples"},
                    {"id": "D", "text": "Stop practicing"},
                ],
                "correct_answer": "A",
                "explanation": "Understanding the basic concept provides a foundation for further learning.",
            },
            {
                "question": f"Which approach is useful for studying {text}?",
                "options": [
                    {"id": "A", "text": "Memorize everything without understanding"},
                    {"id": "B", "text": "Learn step by step and practice"},
                    {"id": "C", "text": "Avoid practical examples"},
                    {"id": "D", "text": "Skip revision"},
                ],
                "correct_answer": "B",
                "explanation": "Step-by-step learning combined with practice helps reinforce understanding.",
            },
            {
                "question": f"Why are examples useful when learning {text}?",
                "options": [
                    {"id": "A", "text": "They make concepts more concrete"},
                    {"id": "B", "text": "They replace all theory"},
                    {"id": "C", "text": "They make practice unnecessary"},
                    {"id": "D", "text": "They remove the need to learn basics"},
                ],
                "correct_answer": "A",
                "explanation": "Examples connect abstract concepts to practical situations.",
            },
        ],
    )


def demo_learning_path(text: str) -> LearningPathResponse:
    return LearningPathResponse(
        topic=text,
        goal=f"Build a strong understanding of {text} from basics to advanced concepts.",
        steps=[
            {
                "level": "Beginner",
                "topics":[
                    f"Introduction to {text}",
                    "Basic terminology",
                    "Core concepts",
                ],
                "suggested_time": "3-5 days",
                "resources": [
                    "Beginner tutorials",
                    "Basic documentation",
                    "Simple practice exercises",
                ],
            },
            {
                "level": "Intermediate",
                "topics": [
                    f"Intermediate {text} concepts",
                    "Practical examples",
                    "Hands-on exercises",
                ],
                "suggested_time": "1-2 weeks",
                "resources": [
                    "Intermediate tutorials",
                    "Practice projects",
                    "Technical documentation",
                ],
            },
            {
                "level": "Advanced",
                "topics": [
                    f"Advanced {text} concepts",
                    "Real-world applications",
                    "Advanced projects",
                ],
                "suggested_time": "2-4 weeks",
                "resources": [
                    "Advanced documentation",
                    "Project-based learning",
                    "Case studies",
                ],
            },
        ],
    )