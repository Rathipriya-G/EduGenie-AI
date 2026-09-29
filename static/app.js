/* =========================================================
   COMMON HELPERS
   ========================================================= */

function escapeHtml(value) {
    return String(value)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
}


function setStatus(element, message, error = false) {
    element.textContent = message;

    element.classList.remove(
        "hidden",
        "error"
    );

    if (error) {
        element.classList.add("error");
    }
}


function clearStatus(element) {
    element.classList.add("hidden");
    element.classList.remove("error");
    element.textContent = "";
}


function showResult(element, html) {
    element.innerHTML = html;
    element.classList.remove("hidden");
}


function hideResult(element) {
    element.innerHTML = "";
    element.classList.add("hidden");
}


/* =========================================================
   GENERIC API REQUEST
   ========================================================= */

async function sendRequest(
    route,
    input,
    statusElement,
    resultElement,
    renderFunction
) {
    const value = input.value.trim();

    if (value.length < 2) {
        setStatus(
            statusElement,
            "Please enter at least 2 characters.",
            true
        );
        return;
    }

    setStatus(
        statusElement,
        "EduGenie is thinking..."
    );

    hideResult(resultElement);

    try {
        const response = await fetch(
            route,
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    text: value
                })
            }
        );

        const data = await response.json();

        if (!response.ok) {
            throw new Error(
                data.detail ||
                "The request could not be completed."
            );
        }

        clearStatus(statusElement);

        showResult(
            resultElement,
            renderFunction(data)
        );

    } catch (error) {
        setStatus(
            statusElement,
            error.message ||
            "Something went wrong.",
            true
        );
    }
}


/* =========================================================
   TEXT RESULT
   ========================================================= */

function renderTextResult(data) {
    let text = escapeHtml(data.result);

    // Headings
    text = text.replace(
        /^### (.+)$/gm,
        "<h3>$1</h3>"
    );

    text = text.replace(
        /^## (.+)$/gm,
        "<h3>$1</h3>"
    );

    text = text.replace(
        /^# (.+)$/gm,
        "<h3>$1</h3>"
    );

    // Bold text
    text = text.replace(
        /\*\*(.+?)\*\*/g,
        "<strong>$1</strong>"
    );

    // Italic text
    text = text.replace(
        /(?<!\*)\*([^*]+)\*(?!\*)/g,
        "<em>$1</em>"
    );

    // Horizontal lines
    text = text.replace(
        /^---$/gm,
        "<hr>"
    );

    // Bullet points
    text = text.replace(
        /^\* (.+)$/gm,
        "<li>$1</li>"
    );

    text = text.replace(
        /^- (.+)$/gm,
        "<li>$1</li>"
    );

    // Numbered lists
    text = text.replace(
        /^\d+\.\s+(.+)$/gm,
        "<li>$1</li>"
    );

    // Group consecutive list items
    text = text.replace(
        /((?:<li>.*<\/li>\s*)+)/gs,
        "<ul>$1</ul>"
    );

    // Blockquotes
    text = text.replace(
        /^&gt; (.+)$/gm,
        "<blockquote>$1</blockquote>"
    );

    // Paragraph breaks
    text = text.replace(
        /\n{2,}/g,
        "</p><p>"
    );

    return `
        <div class="answer">
            <p>${text}</p>
        </div>
    `;
}


/* =========================================================
   QUIZ RESULT
   ========================================================= */

function renderQuiz(result) {
    if (
        !result ||
        !Array.isArray(result.questions)
    ) {
        return "<p>Quiz could not be generated.</p>";
    }

    return `
        <div class="quiz-container">

            <h3>
                ${escapeHtml(
                    result.title ||
                    "EduGenie Quiz"
                )}
            </h3>

            ${result.questions.map(
                (question, index) => `

                    <div
                        class="quiz-question"
                        data-question-index="${index}"
                    >

                        <h4>
                            ${index + 1}.
                            ${escapeHtml(
                                question.question
                            )}
                        </h4>

                        <div class="quiz-options">

                            ${question.options.map(
                                option => `

                                    <label
                                        class="quiz-option"
                                    >

                                        <input
                                            type="radio"
                                            name="quiz-question-${index}"
                                            value="${escapeHtml(
                                                option.id
                                            )}"
                                        >

                                        <span>
                                            <strong>
                                                ${escapeHtml(
                                                    option.id
                                                )}.
                                            </strong>

                                            ${escapeHtml(
                                                option.text
                                            )}
                                        </span>

                                    </label>

                                `
                            ).join("")}

                        </div>

                        <button
                            type="button"
                            class="check-answer-btn"
                            data-question-index="${index}"
                        >
                            Check Answer
                        </button>

                        <div
                            class="quiz-feedback hidden"
                            id="quiz-feedback-${index}"
                        ></div>

                    </div>

                `
            ).join("")}

        </div>
    `;
}


/* =========================================================
   LEARNING PATH RESULT
   ========================================================= */

function renderLearningPath(data) {

    return `
        <div class="learning-goal">

            <h3>
                Learning Goal
            </h3>

            <p>
                ${escapeHtml(data.goal)}
            </p>

        </div>


        ${data.steps
            .map(
                step => `

                    <article class="learning-step">

                        <h3>
                            ${escapeHtml(
                                step.level
                            )}
                        </h3>


                        <p>

                            <strong>
                                Suggested time:
                            </strong>

                            ${escapeHtml(
                                step.suggested_time
                            )}

                        </p>


                        <h4>
                            Topics
                        </h4>

                        <ul>

                            ${step.topics
                                .map(
                                    topic => `

                                        <li>
                                            ${escapeHtml(
                                                topic
                                            )}
                                        </li>

                                    `
                                )
                                .join("")}

                        </ul>


                        <h4>
                            Resources
                        </h4>

                        <ul>

                            ${step.resources
                                .map(
                                    resource => `

                                        <li>
                                            ${escapeHtml(
                                                resource
                                            )}
                                        </li>

                                    `
                                )
                                .join("")}

                        </ul>

                    </article>

                `
            )
            .join("")}
    `;
}


/* =========================================================
   DOM CONTENT LOADED
   ========================================================= */

document.addEventListener(
    "DOMContentLoaded",
    () => {

        /* =================================================
           Q&A
           ================================================= */

        const qaInput =
            document.getElementById("qaInput");

        const qaBtn =
            document.getElementById("qaBtn");

        const qaStatus =
            document.getElementById("qaStatus");

        const qaResult =
            document.getElementById("qaResult");


        qaBtn.addEventListener(
            "click",
            async () => {

                qaBtn.disabled = true;

                await sendRequest(
                    "/api/qa",
                    qaInput,
                    qaStatus,
                    qaResult,
                    renderTextResult
                );

                qaBtn.disabled = false;
            }
        );


        /* =================================================
           QUIZ ANSWER CHECKING
           ================================================= */

        document.addEventListener(
            "click",
            (event) => {

                if (
                    !event.target.classList.contains(
                        "check-answer-btn"
                    )
                ) {
                    return;
                }


                const button =
                    event.target;


                const questionIndex =
                    button.dataset.questionIndex;


                const questionCard =
                    button.closest(
                        ".quiz-question"
                    );


                const selected =
                    questionCard.querySelector(
                        `input[name="quiz-question-${questionIndex}"]:checked`
                    );


                const feedback =
                    questionCard.querySelector(
                        ".quiz-feedback"
                    );


                if (!selected) {

                    feedback.classList.remove(
                        "hidden"
                    );

                    feedback.innerHTML = `
                        <p>
                            Please select an answer first.
                        </p>
                    `;

                    return;
                }


                const questions =
                    window.currentQuizQuestions;


                if (
                    !questions ||
                    !questions[questionIndex]
                ) {

                    feedback.classList.remove(
                        "hidden"
                    );

                    feedback.innerHTML = `
                        <p>
                            Unable to check this answer.
                            Please generate the quiz again.
                        </p>
                    `;

                    return;
                }


                const question =
                    questions[questionIndex];


                feedback.classList.remove(
                    "hidden"
                );


                if (
                    selected.value ===
                    question.correct_answer
                ) {

                    feedback.innerHTML = `
                        <p>
                            <strong>
                                Correct!
                            </strong>
                            🎉
                        </p>

                        <p>
                            ${escapeHtml(
                                question.explanation
                            )}
                        </p>
                    `;

                } else {

                    feedback.innerHTML = `
                        <p>
                            <strong>
                                Incorrect.
                            </strong>
                        </p>

                        <p>
                            Correct answer:
                            <strong>
                                ${escapeHtml(
                                    question.correct_answer
                                )}
                            </strong>
                        </p>

                        <p>
                            ${escapeHtml(
                                question.explanation
                            )}
                        </p>
                    `;
                }
            }
        );


        /* =================================================
           EXPLANATION
           ================================================= */

        const explainInput =
            document.getElementById(
                "explainInput"
            );

        const explainBtn =
            document.getElementById(
                "explainBtn"
            );

        const explainStatus =
            document.getElementById(
                "explainStatus"
            );

        const explainResult =
            document.getElementById(
                "explainResult"
            );


        explainBtn.addEventListener(
            "click",
            async () => {

                explainBtn.disabled = true;

                await sendRequest(
                    "/api/explain",
                    explainInput,
                    explainStatus,
                    explainResult,
                    renderTextResult
                );

                explainBtn.disabled = false;
            }
        );


        /* =================================================
           SUMMARY
           ================================================= */

        const summaryInput =
            document.getElementById(
                "summaryInput"
            );

        const summaryBtn =
            document.getElementById(
                "summaryBtn"
            );

        const summaryStatus =
            document.getElementById(
                "summaryStatus"
            );

        const summaryResult =
            document.getElementById(
                "summaryResult"
            );


        summaryBtn.addEventListener(
            "click",
            async () => {

                summaryBtn.disabled = true;

                await sendRequest(
                    "/api/summarize",
                    summaryInput,
                    summaryStatus,
                    summaryResult,
                    renderTextResult
                );

                summaryBtn.disabled = false;
            }
        );


        /* =================================================
           QUIZ
           ================================================= */

        const quizInput =
            document.getElementById(
                "quizInput"
            );

        const quizBtn =
            document.getElementById(
                "quizBtn"
            );

        const quizStatus =
            document.getElementById(
                "quizStatus"
            );

        const quizResult =
            document.getElementById(
                "quizResult"
            );


        quizBtn.addEventListener(
            "click",
            async () => {

                quizBtn.disabled = true;


                const value =
                    quizInput.value.trim();


                if (value.length < 2) {

                    setStatus(
                        quizStatus,
                        "Please enter at least 2 characters.",
                        true
                    );

                    quizBtn.disabled = false;

                    return;
                }


                setStatus(
                    quizStatus,
                    "EduGenie is thinking..."
                );


                hideResult(
                    quizResult
                );


                try {

                    const response =
                        await fetch(
                            "/api/quiz",
                            {
                                method: "POST",

                                headers: {
                                    "Content-Type":
                                        "application/json"
                                },

                                body:
                                    JSON.stringify({
                                        text: value
                                    })
                            }
                        );


                    const result =
                        await response.json();


                    if (!response.ok) {

                        throw new Error(
                            result.detail ||
                            "Quiz generation failed."
                        );
                    }


                    window.currentQuizQuestions =
                        result.questions;


                    quizResult.innerHTML =
                        renderQuiz(result);


                    quizResult.classList.remove(
                        "hidden"
                    );


                    clearStatus(
                        quizStatus
                    );


                } catch (error) {

                    setStatus(
                        quizStatus,
                        error.message ||
                        "Quiz generation failed.",
                        true
                    );


                    hideResult(
                        quizResult
                    );


                } finally {

                    quizBtn.disabled = false;
                }
            }
        );


        /* =================================================
           LEARNING RECOMMENDATIONS
           ================================================= */

        const learnInput =
            document.getElementById(
                "learnInput"
            );

        const learnBtn =
            document.getElementById(
                "learnBtn"
            );

        const learnStatus =
            document.getElementById(
                "learnStatus"
            );

        const learnResult =
            document.getElementById(
                "learnResult"
            );


        learnBtn.addEventListener(
            "click",
            async () => {

                learnBtn.disabled = true;

                await sendRequest(
                    "/api/learn/recommendations",
                    learnInput,
                    learnStatus,
                    learnResult,
                    renderLearningPath
                );

                learnBtn.disabled = false;
            }
        );

    }
);