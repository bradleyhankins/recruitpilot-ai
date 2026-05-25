from core.review_logic import (
    extract_job_terms,
    followup_questions,
    next_human_review_step,
    review_resume,
    run_review_workflow,
)
from data.sample_data import RESPONSIBLE_USE_NOTE


def test_extract_job_terms_includes_role_relevant_terms():
    terms = extract_job_terms(
        "Need field sales experience, CRM usage, customer follow-up, and appointment setting.",
        "Field Sales",
    )

    assert "sales" in terms
    assert "crm" in terms
    assert "customer" in terms


def test_review_resume_returns_high_review_priority_for_strong_overlap():
    job_description = "Field sales role requiring CRM, customer follow-up, appointment setting, prospecting, lead tracking, presentations, and outbound communication."
    resume_text = "Experienced in sales, CRM, customer follow-up, appointment setting, prospecting, lead tracking, presentations, outbound calls, and homeowner communication."

    review = review_resume(job_description, resume_text, "Field Sales")

    assert review["priority"] == "High Review Priority"
    assert review["signal_count"] >= 8
    assert review["coverage"] > 0


def test_next_human_review_step_for_needs_more_information():
    review = {"priority": "Needs More Information"}

    assert next_human_review_step(review) == "Request clarification or additional resume detail before scheduling next steps."


def test_followup_questions_are_limited_and_include_missing_term():
    questions = followup_questions(
        "Field Sales Consultant",
        signals=["crm"],
        missing_terms=["prospecting", "appointment", "closing", "lead", "customer"],
    )

    assert questions
    assert len(questions) <= 8
    assert any("prospecting" in question.lower() for question in questions)


def test_run_review_workflow_returns_expected_keys():
    workflow = run_review_workflow(
        candidate_name="Jordan Miller",
        role_title="Field Sales Consultant",
        pipeline_stage="Resume Review",
        role_type="Field Sales",
        job_description="Looking for field sales, CRM, customer follow-up, appointment setting, prospecting, and presentations.",
        resume_text="Experience with field sales, CRM updates, customer follow-up, appointment setting, prospecting, and presentations.",
        responsible_use_note=RESPONSIBLE_USE_NOTE,
    )

    expected_keys = {"role_title", "review", "questions", "next_step", "summary", "subject", "email"}

    assert expected_keys.issubset(workflow.keys())
    assert workflow["role_title"] == "Field Sales Consultant"
    assert workflow["review"]["priority"] in {
        "High Review Priority",
        "Standard Review Priority",
        "Needs More Information",
        "Manual Review Recommended",
    }
    assert workflow["questions"]
    assert RESPONSIBLE_USE_NOTE in workflow["summary"]
