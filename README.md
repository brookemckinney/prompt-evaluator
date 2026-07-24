# Prompt Evaluator

*A human-centered tool for evaluating prompts before they are submitted to an AI system.*

## Purpose

Good AI outputs begin with more than detailed instructions.

They begin with clear goals, relevant context, meaningful constraints, awareness of stakeholders, and an understanding of what must remain a human judgment.

Prompt Evaluator helps users identify what a prompt communicates—and what it leaves unsaid.

## What It Evaluates

The application reviews prompts across six dimensions:

1. **Goal Clarity** — Is the desired result clear?
2. **Context** — Does the AI have enough relevant background?
3. **Constraints** — Are limits, requirements, or boundaries defined?
4. **Audience** — Is the intended reader or user identified?
5. **Stakeholders** — Are affected people or perspectives considered?
6. **Human Judgment** — Does the prompt clarify what the human must evaluate or decide?

## What the App Produces

After a user enters a prompt, the application provides:

- an overall prompt-readiness score
- a score for each evaluation dimension
- identified strengths
- missing or underdeveloped elements
- potential failure risks
- questions to answer before using the prompt
- a structured template for improving the prompt

## Guiding Principle

> Better prompting is not only about controlling an AI system. It is about clarifying human intent.

## Technology

This application is built with:

- Python
- Streamlit

The initial version uses a transparent, rule-based evaluation method and does not send prompt content to an external AI model.

## Run Locally

Install the required package:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
streamlit run app.py
```

## Project Structure

```text
prompt-evaluator/
├── app.py
├── requirements.txt
├── README.md
├── LICENSE
└── .gitignore
```

## Future Development

Planned additions include:

- optional language-model analysis
- downloadable evaluation reports
- prompt comparison
- organizational prompt standards
- evaluation history
- specialized modes for education, leadership, and workplace use

## Author

**Brooke McKinney**

Human-Centered AI Strategist  
Learning Systems Designer  
Creator of The Engaging Teacher

https://theengagingteacher.com

## Related Projects

- Relational Wonder
- AI Judgment Toolkit
- Human Capability Lab

---

> AI can respond to the words we provide. Human judgment determines whether those words represent the right problem.
