import re
from collections import Counter

from data.sample_data import KEYWORD_LIBRARY


def limit_text(text: str, max_chars: int) -> tuple[str, bool]:
    if len(text) <= max_chars:
        return text, False
    return text[:max_chars], True


def tokenize(text: str) -> list[str]:
    return re.findall(r"[a-zA-Z][a-zA-Z\-]+", text.lower())


def extract_job_terms(job_description: str, role_type: str) -> list[str]:
    tokens = tokenize(job_description)
    counts = Counter(tokens)
    library_terms = KEYWORD_LIBRARY.get(role_type, KEYWORD_LIBRARY["General Business"])
    role_terms_found = [term for term in library_terms if term.lower() in job_description.lower()]
    common_job_terms = [
        word
        for word, _ in counts.most_common(24)
        if len(word) > 4 and word not in {"looking", "seeking", "strong", "experience"}
    ]
    return list(dict.fromkeys(role_terms_found + common_job_terms))[:18]


def review_resume(job_description: str, resume_text: str, role_type: str) -> dict:
    role_terms = KEYWORD_LIBRARY.get(role_type, KEYWORD_LIBRARY["General Business"])
    job_terms = extract_job_terms(job_description, role_type)
    resume_lower = resume_text.lower()
    matched_role_terms = [term for term in role_terms if term.lower() in resume_lower]
    matched_job_terms = [term for term in job_terms if term.lower() in resume_lower]
    missing_job_terms = [term for term in job_terms if term.lower() not in resume_lower]
    unique_matches = list(dict.fromkeys(matched_role_terms + matched_job_terms))
    signal_count = len(unique_matches)
    missing_count = len(missing_job_terms)
    total_terms = max(len(job_terms), 1)
    coverage = round((len(matched_job_terms) / total_terms) * 100)

    if not resume_text.strip():
        priority = "Manual Review Recommended"
        priority_note = "Resume text was not provided or could not be reviewed."
    elif signal_count >= 8 and missing_count <= 6:
        priority = "High Review Priority"
        priority_note = "Resume contains several job-related signals worth human review."
    elif signal_count >= 4:
        priority = "Standard Review Priority"
        priority_note = "Resume contains some relevant signals, but additional review is needed."
    else:
        priority = "Needs More Information"
        priority_note = "Resume text has limited obvious overlap with the job description. Human review should clarify context."

    return {
        "priority": priority,
        "priority_note": priority_note,
        "matched_terms": unique_matches[:12],
        "missing_terms": missing_job_terms[:12],
        "job_terms": job_terms,
        "signal_count": signal_count,
        "missing_count": missing_count,
        "coverage": coverage,
    }


def followup_questions(role_title: str, signals: list[str], missing_terms: list[str]) -> list[str]:
    questions = [
        f"What interests you most about the {role_title} role?",
        "Walk me through the experience on your resume that best connects to this role.",
        "What type of work environment helps you perform at your best?",
        "How do you stay organized with tasks, notes, and follow-up?",
    ]
    if signals:
        questions.append(f"Your resume mentions {signals[0]}. Can you give a specific example of how you used that in a previous role?")
    for term in missing_terms[:4]:
        questions.append(f"Can you share any experience related to {term} that may not be clear on your resume?")
    return questions[:8]


def next_human_review_step(review: dict) -> str:
    if review["priority"] == "High Review Priority":
        return "Schedule a human phone screen to clarify the strongest resume signals."
    if review["priority"] == "Standard Review Priority":
        return "Review missing information, then decide whether a phone screen is warranted."
    if review["priority"] == "Needs More Information":
        return "Request clarification or additional resume detail before scheduling next steps."
    return "Manually review the resume text and job requirements before taking next action."


def manager_summary(candidate_name: str, role_title: str, pipeline_stage: str, review: dict, next_step: str, responsible_use_note: str) -> str:
    name = candidate_name or "Candidate"
    return f"""{name} is currently in the {pipeline_stage} stage for the {role_title} role.

Review Priority: {review['priority']}
Review Signal Count: {review['signal_count']}
Job-Term Coverage: {review['coverage']}%
Next Human Review Step: {next_step}
Summary: {review['priority_note']}

{responsible_use_note}
"""


def candidate_email(candidate_name: str, role_title: str) -> tuple[str, str]:
    name = candidate_name or "there"
    subject = f"Following Up on the {role_title} Opportunity"
    body = f"""Hi {name},

Thank you for your interest in the {role_title} opportunity.

We are reviewing application materials and may follow up with additional questions about your experience, role expectations, and next steps.

Thanks again,
Hiring Team"""
    return subject, body


def run_review_workflow(candidate_name: str, role_title: str, pipeline_stage: str, role_type: str, job_description: str, resume_text: str, responsible_use_note: str) -> dict:
    role_title = role_title or "Open Role"
    review = review_resume(job_description, resume_text, role_type)
    questions = followup_questions(role_title, review["matched_terms"], review["missing_terms"])
    next_step = next_human_review_step(review)
    summary = manager_summary(candidate_name, role_title, pipeline_stage, review, next_step, responsible_use_note)
    subject, email = candidate_email(candidate_name, role_title)
    return {
        "role_title": role_title,
        "review": review,
        "questions": questions,
        "next_step": next_step,
        "summary": summary,
        "subject": subject,
        "email": email,
    }
