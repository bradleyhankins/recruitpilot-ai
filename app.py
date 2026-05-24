import re
from collections import Counter

import streamlit as st

st.set_page_config(page_title="RecruitPilot AI", page_icon="🧑‍💼", layout="wide")

PIPELINE_STAGES = [
    "New Applicant",
    "Resume Review",
    "Phone Screen",
    "Interview Scheduled",
    "Interview Completed",
    "Reference Check",
    "Human Decision Pending",
]

ROLE_TYPES = [
    "Field Sales",
    "Inside Sales",
    "Operations",
    "Customer Success",
    "Project Management",
    "General Business",
]

SAMPLE_DATA = {
    "Blank / Custom": {},
    "Field Sales Resume Review": {
        "candidate_name": "Jordan Miller",
        "role_title": "Field Sales Consultant",
        "role_type": "Field Sales",
        "pipeline_stage": "Resume Review",
        "job_description": "We are looking for a field sales consultant with customer-facing sales experience, strong follow-up habits, CRM usage, comfort with prospecting, appointment setting, and the ability to explain value clearly to homeowners.",
        "resume_text": "Jordan Miller has 4 years of customer-facing sales experience in home services. Experience includes appointment setting, CRM updates, outbound follow-up, lead tracking, customer presentations, and working with homeowners to explain project options.",
    },
    "Operations Resume Review": {
        "candidate_name": "Morgan Ellis",
        "role_title": "Operations Coordinator",
        "role_type": "Operations",
        "pipeline_stage": "Resume Review",
        "job_description": "Seeking an operations coordinator with strong organization, scheduling, CRM or spreadsheet experience, documentation habits, customer communication, and process follow-through.",
        "resume_text": "Morgan Ellis has experience coordinating schedules, managing spreadsheets, updating CRM records, documenting customer notes, and supporting office workflows. Strong organization and communication skills.",
    },
}

KEYWORD_LIBRARY = {
    "Field Sales": ["sales", "prospecting", "follow-up", "crm", "appointment", "customer", "presentation", "closing", "lead", "outbound", "homeowner"],
    "Inside Sales": ["sales", "phone", "email", "crm", "lead", "appointment", "follow-up", "customer", "pipeline", "inbound", "outbound"],
    "Operations": ["operations", "scheduling", "spreadsheet", "crm", "documentation", "process", "coordination", "customer", "office", "workflow"],
    "Customer Success": ["customer", "service", "support", "retention", "follow-up", "communication", "issue", "crm", "experience", "resolution"],
    "Project Management": ["project", "schedule", "coordination", "customer", "vendor", "timeline", "documentation", "scope", "quality", "communication"],
    "General Business": ["customer", "communication", "organization", "crm", "process", "follow-up", "team", "documentation", "sales", "operations"],
}

CUSTOM_CSS = """
<style>
.block-container { max-width: 1180px; padding-top: 1.35rem; padding-bottom: 3rem; }
[data-testid="stSidebar"] { background: #111827; }
[data-testid="stSidebar"] h1,[data-testid="stSidebar"] h2,[data-testid="stSidebar"] h3,[data-testid="stSidebar"] p,[data-testid="stSidebar"] span,[data-testid="stSidebar"] label,[data-testid="stSidebar"] li { color: #f9fafb !important; }
[data-testid="stSidebar"] li::marker { color: #93c5fd !important; }
.hero { padding: 1.9rem 2rem; border-radius: 20px; background: linear-gradient(135deg, #111827 0%, #1f2937 52%, #334155 100%); color: #ffffff; box-shadow: 0 18px 36px rgba(17, 24, 39, .18); margin-bottom: 1rem; }
.eyebrow { text-transform: uppercase; letter-spacing: .13em; font-size: .75rem; font-weight: 800; color: #93c5fd; margin-bottom: .65rem; }
.hero-title { font-size: 2.25rem; line-height: 1.08; font-weight: 850; margin-bottom: .65rem; }
.hero-subtitle { font-size: 1.02rem; line-height: 1.62; color: #e5e7eb; max-width: 900px; }
.hero-pills span { display: inline-block; padding: .35rem .65rem; margin: .75rem .28rem 0 0; border-radius: 999px; background: rgba(255,255,255,.10); border: 1px solid rgba(255,255,255,.16); font-weight: 700; font-size: .78rem; color: #f8fafc; }
.section-title { margin-top: 1.25rem; margin-bottom: .55rem; font-size: 1.4rem; font-weight: 850; color: #111827; }
.section-lede { color: #4b5563; line-height: 1.6; margin-bottom: 1rem; max-width: 950px; }
.form-group-title { font-size: .9rem; font-weight: 850; text-transform: uppercase; letter-spacing: .06em; color: #64748b; margin: .35rem 0 .15rem 0; }
.metric-card,.output-card,.signal-card,.warning-card { background: #ffffff; border: 1px solid #e5e7eb; border-radius: 18px; box-shadow: 0 8px 20px rgba(15,23,42,.055); }
.metric-card { height: 138px; padding: 1rem; margin-bottom: .75rem; }
.metric-label { color: #6b7280; font-size: .78rem; font-weight: 800; text-transform: uppercase; letter-spacing: .05em; margin-bottom: .5rem; }
.metric-value { color: #111827; font-size: 1.35rem; line-height: 1.18; font-weight: 900; overflow-wrap: break-word; }
.metric-note { color: #64748b; font-size: .85rem; margin-top: .55rem; }
.output-card,.signal-card,.warning-card { padding: 1.15rem; margin-bottom: .8rem; }
.output-card { border-left: 5px solid #111827; }
.signal-card { border-left: 5px solid #059669; }
.warning-card { border-left: 5px solid #f59e0b; }
.output-card h3,.signal-card h3,.warning-card h3 { font-size: 1.05rem; font-weight: 850; color: #111827; margin-bottom: .4rem; }
.output-card p,.signal-card p,.warning-card p,.output-card li,.signal-card li,.warning-card li { color: #4b5563; line-height: 1.52; font-size: .93rem; }
.note-box { padding: .9rem 1rem; border-radius: 14px; background: #f8fafc; color: #334155; border: 1px solid #e2e8f0; font-weight: 650; margin: .9rem 0; font-size: .92rem; }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


def section_title(title, lede=None):
    st.markdown(f'<div class="section-title">{title}</div>', unsafe_allow_html=True)
    if lede:
        st.markdown(f'<div class="section-lede">{lede}</div>', unsafe_allow_html=True)


def form_group(title):
    st.markdown(f'<div class="form-group-title">{title}</div>', unsafe_allow_html=True)


def metric_card(label, value, note=None):
    note_html = f'<div class="metric-note">{note}</div>' if note else ""
    st.markdown(f'<div class="metric-card"><div class="metric-label">{label}</div><div class="metric-value">{value}</div>{note_html}</div>', unsafe_allow_html=True)


def html_card(title, body, css_class="output-card"):
    st.markdown(f'<div class="{css_class}"><h3>{title}</h3>{body}</div>', unsafe_allow_html=True)


def tokenize(text):
    return re.findall(r"[a-zA-Z][a-zA-Z\-]+", text.lower())


def extract_job_terms(job_description, role_type):
    tokens = tokenize(job_description)
    counts = Counter(tokens)
    library_terms = KEYWORD_LIBRARY.get(role_type, KEYWORD_LIBRARY["General Business"])
    jd_terms = [term for term in library_terms if term.lower() in job_description.lower()]
    common_terms = [word for word, _ in counts.most_common(20) if len(word) > 4]
    return list(dict.fromkeys(jd_terms + common_terms))[:18]


def review_resume(job_description, resume_text, role_type):
    role_terms = KEYWORD_LIBRARY.get(role_type, KEYWORD_LIBRARY["General Business"])
    job_terms = extract_job_terms(job_description, role_type)
    resume_lower = resume_text.lower()

    matched_role_terms = [term for term in role_terms if term.lower() in resume_lower]
    matched_job_terms = [term for term in job_terms if term.lower() in resume_lower]
    missing_job_terms = [term for term in job_terms if term.lower() not in resume_lower]

    unique_matches = list(dict.fromkeys(matched_role_terms + matched_job_terms))
    review_signal_count = len(unique_matches)
    missing_count = len(missing_job_terms)

    if review_signal_count >= 8 and missing_count <= 6:
        priority = "High Review Priority"
        priority_note = "Resume contains several job-related signals worth human review."
    elif review_signal_count >= 4:
        priority = "Standard Review Priority"
        priority_note = "Resume contains some relevant signals, but additional review is needed."
    elif resume_text.strip():
        priority = "Needs More Information"
        priority_note = "Resume text has limited obvious overlap with the job description. Human review should clarify context."
    else:
        priority = "Manual Review Recommended"
        priority_note = "Resume text was not provided or could not be reviewed."

    return {
        "priority": priority,
        "priority_note": priority_note,
        "matched_terms": unique_matches[:12],
        "missing_terms": missing_job_terms[:12],
        "review_signal_count": review_signal_count,
        "missing_count": missing_count,
    }


def followup_questions(role_title, signals, missing_terms):
    questions = [
        f"What interests you most about the {role_title} role?",
        "Walk me through the experience on your resume that best connects to this role.",
        "What type of work environment helps you perform at your best?",
        "How do you stay organized with tasks, notes, and follow-up?",
    ]
    for term in missing_terms[:4]:
        questions.append(f"Can you share any experience related to {term} that may not be clear on your resume?")
    if signals:
        questions.append(f"Your resume mentions {signals[0]}. Can you give a specific example of how you used that in a previous role?")
    return questions[:8]


def manager_summary(candidate_name, role_title, pipeline_stage, review):
    name = candidate_name or "Candidate"
    return f"""{name} is currently in the {pipeline_stage} stage for the {role_title} role.

Review Priority: {review['priority']}
Summary: {review['priority_note']}

This packet is intended to organize resume signals and missing information for human review. It should not be used as the sole basis for selection, rejection, compensation, or employment decisions.
"""


def candidate_email(candidate_name, role_title):
    name = candidate_name or "there"
    subject = f"Following Up on the {role_title} Opportunity"
    body = f"""Hi {name},

Thank you for your interest in the {role_title} opportunity.

We are reviewing application materials and may follow up with additional questions about your experience, role expectations, and next steps.

Thanks again,
Hiring Team"""
    return subject, body


def build_report(candidate_name, role_title, role_type, pipeline_stage, job_description, resume_text, review, questions, summary, subject, email):
    signal_lines = "\n".join(f"- {item}" for item in review["matched_terms"]) or "- No clear match signals found from the provided text."
    missing_lines = "\n".join(f"- {item}" for item in review["missing_terms"]) or "- No major missing terms identified from the provided job description."
    question_lines = "\n".join(f"{index + 1}. {question}" for index, question in enumerate(questions))
    return f"""# RecruitPilot AI Resume Review Packet

## Candidate Tracking
Candidate: {candidate_name or 'N/A'}
Role Title: {role_title}
Role Type: {role_type}
Pipeline Stage: {pipeline_stage}
Review Priority: {review['priority']}

## Responsible Use Note
This tool organizes resume information for human review. It should not be used as the sole basis for selection, rejection, compensation, or employment decisions.

## Job Description
{job_description or 'No job description provided.'}

## Resume Text Reviewed
{resume_text or 'No resume text provided.'}

## Resume Match Signals
{signal_lines}

## Missing / Unclear Information
{missing_lines}

## Suggested Follow-Up Questions
{question_lines}

## Manager Review Summary
{summary}

## Candidate Follow-Up Email
Subject: {subject}

{email}

---

Generated by RecruitPilot AI.
"""


with st.sidebar:
    st.title("RecruitPilot AI")
    st.caption("Version 2.0")
    st.markdown("ATS Lite resume review assistant for organizing applicant information before human review.")
    st.divider()
    st.markdown("### Outputs")
    st.markdown("- Pipeline stage\n- Review priority\n- Resume match signals\n- Missing information\n- Follow-up questions\n- Manager summary\n- Candidate email\n- Downloadable packet")

st.markdown("""
<div class="hero">
    <div class="eyebrow">ATS Lite Resume Review Assistant</div>
    <div class="hero-title">RecruitPilot AI</div>
    <div class="hero-subtitle">Organize job descriptions and resume text into review priorities, match signals, missing information, follow-up questions, and manager-ready review packets.</div>
    <div class="hero-pills"><span>ATS Lite</span><span>Resume Review</span><span>Pipeline Tracking</span><span>Interview Prep</span><span>Streamlit</span></div>
</div>
""", unsafe_allow_html=True)

section_title("Resume review builder", "Load a fictional sample or paste a job description and resume text. This tool supports human review and does not make employment decisions.")

scenario_name = st.selectbox("Load Sample Scenario", list(SAMPLE_DATA.keys()))
scenario = SAMPLE_DATA.get(scenario_name, {})

with st.form("resume_review_form"):
    form_group("Candidate and pipeline details")
    col1, col2, col3 = st.columns(3)
    with col1:
        candidate_name = st.text_input("Candidate Name", value=scenario.get("candidate_name", ""), placeholder="Example: Jordan Miller")
    with col2:
        role_title = st.text_input("Role Title", value=scenario.get("role_title", ""), placeholder="Example: Field Sales Consultant")
    with col3:
        pipeline_stage = st.selectbox("Pipeline Stage", PIPELINE_STAGES, index=PIPELINE_STAGES.index(scenario.get("pipeline_stage", "Resume Review")))

    role_type = st.selectbox("Role Type", ROLE_TYPES, index=ROLE_TYPES.index(scenario.get("role_type", "Field Sales")))

    form_group("Job description and resume text")
    job_description = st.text_area("Job Description / Role Requirements", value=scenario.get("job_description", ""), height=150)
    resume_text = st.text_area("Resume Text", value=scenario.get("resume_text", ""), height=180)

    submitted = st.form_submit_button("Generate Resume Review Packet", use_container_width=True)

if not submitted:
    st.markdown('<div class="note-box">Paste a job description and resume text, or load a sample scenario, then generate the review packet.</div>', unsafe_allow_html=True)
    st.stop()

review = review_resume(job_description, resume_text, role_type)
questions = followup_questions(role_title or "the open role", review["matched_terms"], review["missing_terms"])
summary = manager_summary(candidate_name, role_title or "Open Role", pipeline_stage, review)
subject, email = candidate_email(candidate_name, role_title or "Open Role")
report = build_report(candidate_name, role_title or "Open Role", role_type, pipeline_stage, job_description, resume_text, review, questions, summary, subject, email)

section_title("Review snapshot")
s1, s2, s3, s4 = st.columns(4)
with s1:
    metric_card("Review Priority", review["priority"])
with s2:
    metric_card("Pipeline Stage", pipeline_stage)
with s3:
    metric_card("Match Signals", str(review["review_signal_count"]))
with s4:
    metric_card("Missing Items", str(review["missing_count"]))

html_card("Responsible Use Note", "<p>This tool organizes resume information for human review. It should not be used as the sole basis for selection, rejection, compensation, or employment decisions.</p>", "warning-card")
html_card("Review Priority Explanation", f"<p>{review['priority_note']}</p>", "output-card")

section_title("Resume match signals and missing information")
match_col, missing_col = st.columns(2)
with match_col:
    html_card("Resume Match Signals", "<ul>" + "".join(f"<li>{item}</li>" for item in review["matched_terms"]) + "</ul>", "signal-card")
with missing_col:
    html_card("Missing / Unclear Information", "<ul>" + "".join(f"<li>{item}</li>" for item in review["missing_terms"]) + "</ul>", "warning-card")

section_title("Interview follow-up support")
html_card("Suggested Follow-Up Questions", "<ol>" + "".join(f"<li>{question}</li>" for question in questions) + "</ol>", "output-card")

section_title("Manager and candidate communication")
tab1, tab2 = st.tabs(["Manager Summary", "Candidate Email"])
with tab1:
    st.text_area("Manager-ready summary", summary, height=240)
with tab2:
    st.text_input("Subject Line", subject)
    st.text_area("Candidate email", email, height=220)

section_title("Download review packet")
st.download_button("Download Resume Review Packet", data=report, file_name="recruitpilot-resume-review-packet.md", mime="text/markdown", use_container_width=True)

st.markdown('<div class="note-box">Privacy note: Information entered into this app is processed during the active session and is not saved by this app.</div>', unsafe_allow_html=True)
