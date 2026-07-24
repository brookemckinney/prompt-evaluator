import re
from dataclasses import dataclass
from typing import Callable

import streamlit as st


@dataclass
class EvaluationDimension:
    """Defines one dimension of prompt quality."""

    name: str
    description: str
    evaluator: Callable[[str], tuple[int, str]]


def contains_any(text: str, terms: list[str]) -> bool:
    """Return True when the text contains at least one listed term."""
    lowered = text.lower()
    return any(term in lowered for term in terms)


def count_matches(text: str, terms: list[str]) -> int:
    """Count how many listed terms appear in the text."""
    lowered = text.lower()
    return sum(1 for term in terms if term in lowered)


def evaluate_goal(prompt: str) -> tuple[int, str]:
    action_terms = [
        "write",
        "create",
        "analyze",
        "compare",
        "evaluate",
        "summarize",
        "design",
        "recommend",
        "identify",
        "explain",
        "develop",
        "revise",
        "draft",
        "produce",
        "generate",
    ]

    score = 0

    if contains_any(prompt, action_terms):
        score += 5

    if len(prompt.split()) >= 12:
        score += 3

    if contains_any(
        prompt,
        ["goal", "objective", "outcome", "purpose", "help me", "i need", "i want"],
    ):
        score += 2

    if score >= 8:
        feedback = "The requested action and intended result are reasonably clear."
    elif score >= 5:
        feedback = "An action is present, but the desired outcome could be more specific."
    else:
        feedback = "The prompt does not clearly define what should be produced or accomplished."

    return min(score, 10), feedback


def evaluate_context(prompt: str) -> tuple[int, str]:
    context_terms = [
        "context",
        "background",
        "currently",
        "because",
        "situation",
        "project",
        "organization",
        "course",
        "team",
        "client",
        "company",
        "student",
        "audience",
        "we are",
        "i am",
    ]

    matches = count_matches(prompt, context_terms)
    score = min(matches * 2, 8)

    if len(prompt.split()) >= 45:
        score += 2
    elif len(prompt.split()) >= 25:
        score += 1

    if score >= 7:
        feedback = "The prompt supplies useful background for interpreting the task."
    elif score >= 4:
        feedback = "Some context is present, but important background may still be missing."
    else:
        feedback = "The AI may have to guess about the situation, purpose, or surrounding conditions."

    return min(score, 10), feedback


def evaluate_constraints(prompt: str) -> tuple[int, str]:
    constraint_terms = [
        "must",
        "should",
        "do not",
        "avoid",
        "limit",
        "maximum",
        "minimum",
        "no more than",
        "at least",
        "format",
        "length",
        "tone",
        "deadline",
        "include",
        "exclude",
        "only",
        "without",
    ]

    matches = count_matches(prompt, constraint_terms)
    score = min(matches * 2, 10)

    if score >= 7:
        feedback = "The prompt defines meaningful requirements or boundaries."
    elif score >= 4:
        feedback = "Some requirements are present, but the boundaries could be more precise."
    else:
        feedback = "The response may vary widely because few constraints are defined."

    return score, feedback


def evaluate_audience(prompt: str) -> tuple[int, str]:
    audience_terms = [
        "audience",
        "reader",
        "user",
        "customer",
        "client",
        "student",
        "faculty",
        "leader",
        "executive",
        "manager",
        "employee",
        "beginner",
        "expert",
        "public",
        "parents",
        "teachers",
        "team",
    ]

    score = min(count_matches(prompt, audience_terms) * 3, 9)

    if contains_any(prompt, ["for a", "for an", "intended for", "written for"]):
        score += 1

    if score >= 7:
        feedback = "The intended audience is identifiable."
    elif score >= 4:
        feedback = "A possible audience is implied but not fully described."
    else:
        feedback = "The prompt does not clearly identify who will use or receive the output."

    return min(score, 10), feedback


def evaluate_stakeholders(prompt: str) -> tuple[int, str]:
    stakeholder_terms = [
        "stakeholder",
        "affected",
        "impact",
        "perspective",
        "community",
        "employee",
        "student",
        "customer",
        "client",
        "leader",
        "team",
        "family",
        "patient",
        "faculty",
        "partner",
        "risk",
        "benefit",
    ]

    score = min(count_matches(prompt, stakeholder_terms) * 2, 10)

    if score >= 7:
        feedback = "The prompt recognizes people, perspectives, or groups affected by the task."
    elif score >= 4:
        feedback = "Some affected people are visible, but other perspectives may be missing."
    else:
        feedback = "The prompt may overlook people affected by the output or decision."

    return score, feedback


def evaluate_human_judgment(prompt: str) -> tuple[int, str]:
    judgment_terms = [
        "judgment",
        "decision",
        "decide",
        "verify",
        "evaluate",
        "review",
        "approve",
        "responsible",
        "responsibility",
        "tradeoff",
        "uncertainty",
        "recommendation",
        "do not decide",
        "human",
        "final choice",
        "evidence",
    ]

    score = min(count_matches(prompt, judgment_terms) * 2, 10)

    if score >= 7:
        feedback = "The prompt makes human evaluation or decision responsibility visible."
    elif score >= 4:
        feedback = "Human review is implied, but responsibility could be stated more directly."
    else:
        feedback = "The prompt does not explain what a human must verify, interpret, or decide."

    return score, feedback


DIMENSIONS = [
    EvaluationDimension(
        "Goal Clarity",
        "How clearly the prompt defines the task and desired result.",
        evaluate_goal,
    ),
    EvaluationDimension(
        "Context",
        "Whether the prompt provides relevant background.",
        evaluate_context,
    ),
    EvaluationDimension(
        "Constraints",
        "Whether requirements, limits, and boundaries are defined.",
        evaluate_constraints,
    ),
    EvaluationDimension(
        "Audience",
        "Whether the intended reader or user is identifiable.",
        evaluate_audience,
    ),
    EvaluationDimension(
        "Stakeholders",
        "Whether affected people and perspectives are considered.",
        evaluate_stakeholders,
    ),
    EvaluationDimension(
        "Human Judgment",
        "Whether human verification, interpretation, or responsibility remains visible.",
        evaluate_human_judgment,
    ),
]


def build_improvement_questions(scores: dict[str, int]) -> list[str]:
    questions = []

    if scores["Goal Clarity"] < 7:
        questions.append("What exact output or decision do you need?")

    if scores["Context"] < 7:
        questions.append("What background would change how the task should be understood?")

    if scores["Constraints"] < 7:
        questions.append("What requirements, boundaries, or exclusions must be followed?")

    if scores["Audience"] < 7:
        questions.append("Who will read, use, or be affected by the result?")

    if scores["Stakeholders"] < 7:
        questions.append("Whose perspective or experience may be missing?")

    if scores["Human Judgment"] < 7:
        questions.append("What must a human verify, evaluate, or decide?")

    return questions


def build_risks(scores: dict[str, int]) -> list[str]:
    risks = []

    if scores["Goal Clarity"] < 5:
        risks.append("The AI may solve the wrong problem.")

    if scores["Context"] < 5:
        risks.append("The response may rely on invented or generic assumptions.")

    if scores["Constraints"] < 5:
        risks.append("The output may be unusable because requirements are undefined.")

    if scores["Audience"] < 5:
        risks.append("The tone, detail, or format may not fit the intended user.")

    if scores["Stakeholders"] < 5:
        risks.append("The response may overlook consequences for affected people.")

    if scores["Human Judgment"] < 5:
        risks.append("A recommendation may appear more authoritative than it should.")

    if not risks:
        risks.append(
            "No major structural risks were detected, but factual claims should still be verified."
        )

    return risks


def create_prompt_template(original_prompt: str) -> str:
    return f"""GOAL
Describe the exact result or decision needed.

CONTEXT
Provide the background, situation, and information the AI would not otherwise know.

AUDIENCE
Identify who will read, use, or be affected by the output.

REQUIREMENTS
List the required content, format, tone, length, and other constraints.

STAKEHOLDERS
Identify relevant perspectives, risks, and people who may be affected.

HUMAN JUDGMENT
State what must be verified, interpreted, approved, or decided by a human.

ORIGINAL REQUEST
{original_prompt.strip()}
"""


st.set_page_config(
    page_title="Prompt Evaluator",
    page_icon="🧭",
    layout="wide",
)

st.title("Prompt Evaluator")
st.subheader("Evaluate what your prompt communicates—and what it leaves unsaid.")

st.markdown(
    """
This tool evaluates prompts across six dimensions of human-centered prompt design.
It uses transparent rules and does **not** send your text to an external AI model.
"""
)

example_prompt = (
    "Create a one-page briefing for university leaders explaining three risks "
    "of adopting generative AI without faculty training. Use a professional but "
    "accessible tone. Include recommended next steps, identify affected stakeholders, "
    "flag uncertain claims, and leave the final policy decision to institutional leaders."
)

prompt = st.text_area(
    "Paste your prompt",
    height=220,
    placeholder="Enter the prompt you want to evaluate...",
)

col1, col2 = st.columns([1, 1])

with col1:
    evaluate_clicked = st.button(
        "Evaluate prompt",
        type="primary",
        use_container_width=True,
    )

with col2:
    example_clicked = st.button(
        "Load example",
        use_container_width=True,
    )

if example_clicked:
    st.session_state["loaded_example"] = example_prompt
    st.rerun()

if "loaded_example" in st.session_state and not prompt:
    prompt = st.session_state.pop("loaded_example")

if evaluate_clicked:
    if not prompt.strip():
        st.warning("Enter a prompt before running the evaluation.")
    else:
        results = {}
        feedback = {}

        for dimension in DIMENSIONS:
            score, explanation = dimension.evaluator(prompt)
            results[dimension.name] = score
            feedback[dimension.name] = explanation

        overall_score = round(sum(results.values()) / len(results), 1)

        st.divider()
        st.header("Evaluation")

        score_col, summary_col = st.columns([1, 2])

        with score_col:
            st.metric("Overall readiness", f"{overall_score}/10")
            st.progress(overall_score / 10)

        with summary_col:
            if overall_score >= 8:
                st.success(
                    "This prompt is well structured. Review factual accuracy and "
                    "human decision responsibility before using the output."
                )
            elif overall_score >= 6:
                st.info(
                    "This prompt has a useful foundation but would benefit from "
                    "additional context or clearer boundaries."
                )
            else:
                st.warning(
                    "This prompt leaves important decisions to inference. Strengthen "
                    "it before relying on the resulting output."
                )

        st.subheader("Dimension scores")

        for dimension in DIMENSIONS:
            score = results[dimension.name]

            with st.expander(
                f"{dimension.name}: {score}/10",
                expanded=True,
            ):
                st.write(dimension.description)
                st.progress(score / 10)
                st.write(feedback[dimension.name])

        st.subheader("Potential failure risks")

        for risk in build_risks(results):
            st.write(f"- {risk}")

        questions = build_improvement_questions(results)

        st.subheader("Questions to answer")

        if questions:
            for question in questions:
                st.write(f"- {question}")
        else:
            st.write(
                "The prompt addresses all six dimensions. Confirm that its factual "
                "inputs and assumptions are accurate."
            )

        st.subheader("Improvement template")

        improved_template = create_prompt_template(prompt)

        st.code(improved_template, language="text")

        st.download_button(
            label="Download improvement template",
            data=improved_template,
            file_name="improved-prompt-template.txt",
            mime="text/plain",
        )

st.divider()

st.caption(
    "Prompt Evaluator is a human-centered AI enablement project by Brooke McKinney."
)
