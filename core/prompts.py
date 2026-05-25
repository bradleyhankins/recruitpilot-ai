import re


def build_ai_review_prompt(candidate_name, role_title, role_type, pipeline_stage, job_description, resume_text, review, questions, summary, subject, email):
    return f"""
You are an interview preparation assistant for human hiring managers.
Support human review only. Do not rank, reject, select, score, or recommend whether to hire the person.
Do not infer protected characteristics. Do not invent facts not present in the materials.
Improve the manager summary, clarification questions, and candidate communication while preserving responsible-use boundaries.

Candidate: {candidate_name or 'N/A'}
Role title: {role_title}
Role type: {role_type}
Pipeline stage: {pipeline_stage}
Job description:
{job_description}

Resume text:
{resume_text}

Rules-based review:
{review}

Rules-based questions:
{questions}

Rules-based manager summary:
{summary}

Rules-based candidate email subject: {subject}
Rules-based candidate email:
{email}

Return exactly in this format:
MANAGER SUMMARY:
...

FOLLOW-UP QUESTIONS:
1. ...
2. ...

CANDIDATE EMAIL SUBJECT:
...

CANDIDATE EMAIL BODY:
...
"""


def parse_ai_review(raw: str, fallback_summary: str, fallback_questions: list[str], fallback_subject: str, fallback_email: str) -> tuple[str, list[str], str, str]:
    if not raw:
        return fallback_summary, fallback_questions, fallback_subject, fallback_email

    sections = {
        "MANAGER SUMMARY": "summary",
        "FOLLOW-UP QUESTIONS": "questions",
        "CANDIDATE EMAIL SUBJECT": "subject",
        "CANDIDATE EMAIL BODY": "email",
    }
    parsed = {
        "summary": fallback_summary,
        "questions": "\n".join(fallback_questions),
        "subject": fallback_subject,
        "email": fallback_email,
    }
    for heading, key in sections.items():
        start = raw.find(f"{heading}:")
        if start == -1:
            continue
        start += len(f"{heading}:")
        end_candidates = [raw.find(f"{next_heading}:", start) for next_heading in sections if next_heading != heading]
        end_candidates = [idx for idx in end_candidates if idx != -1]
        end = min(end_candidates) if end_candidates else len(raw)
        value = raw[start:end].strip()
        if value:
            parsed[key] = value

    question_lines = [
        re.sub(r"^\d+[.)]\s*", "", line.strip(" -\t"))
        for line in parsed["questions"].splitlines()
        if line.strip()
    ]
    return parsed["summary"], question_lines[:8] or fallback_questions, parsed["subject"], parsed["email"]
