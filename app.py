import streamlit as st

from ai_helpers import enhance_text, stable_cache_key
from core.prompts import build_ai_review_prompt, parse_ai_review
from core.report_builder import build_review_packet, build_tracker_csv
from core.review_logic import limit_text, run_review_workflow
from data.sample_data import (
    MAX_TEXT_CHARS,
    MAX_UPLOAD_BYTES,
    PIPELINE_STAGES,
    PRIVACY_NOTE,
    RESPONSIBLE_USE_NOTE,
    ROLE_TYPES,
    SAMPLE_DATA,
)
from pdf_helpers import markdown_to_pdf

st.set_page_config(page_title="RecruitPilot AI", page_icon="🧑‍💼", layout="wide")

CUSTOM_CSS = """
<style>
.block-container { max-width: 1180px; padding-top: 1.35rem; padding-bottom: 3rem; }
[data-testid="stSidebar"] { background: #111827; }
[data-testid="stSidebar"] h1,[data-testid="stSidebar"] h2,[data-testid="stSidebar"] h3,[data-testid="stSidebar"] p,[data-testid="stSidebar"] span,[data-testid="stSidebar"] label,[data-testid="stSidebar"] li,[data-testid="stSidebar"] ul,[data-testid="stSidebar"] ol { color: #f9fafb !important; }
[data-testid="stSidebar"] li::marker { color: #93c5fd !important; }
.hero { padding: 1.9rem 2rem; border-radius: 20px; background: linear-gradient(135deg, #111827 0%, #1f2937 52%, #334155 100%); color: #ffffff; box-shadow: 0 18px 36px rgba(17, 24, 39, .18); margin-bottom: 1rem; }
.eyebrow { text-transform: uppercase; letter-spacing: .13em; font-size: .75rem; font-weight: 800; color: #93c5fd; margin-bottom: .65rem; }
.hero-title { font-size: 2.25rem; line-height: 1.08; font-weight: 850; margin-bottom: .65rem; }
.hero-subtitle { font-size: 1.02rem; line-height: 1.62; color: #e5e7eb; max-width: 900px; }
.hero-pills span { display: inline-block; padding: .35rem .65rem; margin: .75rem .28rem 0 0; border-radius: 999px; background: rgba(255, 255, 255, .10); border: 1px solid rgba(255, 255, 255, .16); font-weight: 700; font-size: .78rem; color: #f8fafc; }
.section-title { margin-top: 1.25rem; margin-bottom: .55rem; font-size: 1.4rem; font-weight: 850; color: #111827; }
.section-lede { color: #4b5563; line-height: 1.6; margin-bottom: 1rem; max-width: 950px; }
.form-group-title { font-size: .9rem; font-weight: 850; text-transform: uppercase; letter-spacing: .06em; color: #64748b; margin: .35rem 0 .15rem 0; }
.metric-card,.output-card,.signal-card,.warning-card,.workflow-card { background: #ffffff; border: 1px solid #e5e7eb; border-radius: 18px; box-shadow: 0 8px 20px rgba(15, 23, 42, .055); }
.metric-card { height: 138px; padding: 1rem; margin-bottom: .75rem; }
.metric-label { color: #6b7280; font-size: .78rem; font-weight: 800; text-transform: uppercase; letter-spacing: .05em; margin-bottom: .5rem; }
.metric-value { color: #111827; font-size: 1.35rem; line-height: 1.18; font-weight: 900; overflow-wrap: break-word; }
.metric-note { color: #64748b; font-size: .85rem; margin-top: .55rem; }
.output-card,.signal-card,.warning-card,.workflow-card { padding: 1.15rem; margin-bottom: .8rem; }
.output-card { border-left: 5px solid #111827; }
.signal-card { border-left: 5px solid #059669; }
.warning-card { border-left: 5px solid #f59e0b; }
.workflow-card { border-left: 5px solid #1d4ed8; }
.output-card h3,.signal-card h3,.warning-card h3,.workflow-card h3 { font-size: 1.05rem; font-weight: 850; color: #111827; margin-bottom: .4rem; }
.output-card p,.signal-card p,.warning-card p,.workflow-card p,.output-card li,.signal-card li,.warning-card li,.workflow-card li { color: #4b5563; line-height: 1.52; font-size: .93rem; }
.note-box { padding: .9rem 1rem; border-radius: 14px; background: #f8fafc; color: #334155; border: 1px solid #e2e8f0; font-weight: 650; margin: .9rem 0; font-size: .92rem; }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


def section_title(title: str, lede: str | None = None) -> None:
    st.markdown(f'<div class="section-title">{title}</div>', unsafe_allow_html=True)
    if lede:
        st.markdown(f'<div class="section-lede">{lede}</div>', unsafe_allow_html=True)


def form_group(title: str) -> None:
    st.markdown(f'<div class="form-group-title">{title}</div>', unsafe_allow_html=True)


def metric_card(label: str, value: str, note: str | None = None) -> None:
    note_html = f'<div class="metric-note">{note}</div>' if note else ""
    st.markdown(f'<div class="metric-card"><div class="metric-label">{label}</div><div class="metric-value">{value}</div>{note_html}</div>', unsafe_allow_html=True)


def html_card(title: str, body: str, css_class: str = "output-card") -> None:
    st.markdown(f'<div class="{css_class}"><h3>{title}</h3>{body}</div>', unsafe_allow_html=True)


def html_list(items: list[str], empty_message: str) -> str:
    visible_items = items or [empty_message]
    return "<ul>" + "".join(f"<li>{item}</li>" for item in visible_items) + "</ul>"


def decode_uploaded_text(uploaded_file) -> str:
    if uploaded_file is None:
        return ""
    if uploaded_file.size > MAX_UPLOAD_BYTES:
        st.error(f"The uploaded file is too large. Please upload a plain-text resume under {MAX_UPLOAD_BYTES // 1000} KB.")
        st.stop()
    try:
        return uploaded_file.getvalue().decode("utf-8")
    except UnicodeDecodeError:
        return uploaded_file.getvalue().decode("latin-1", errors="ignore")


def render_sidebar() -> None:
    with st.sidebar:
        st.title("RecruitPilot AI")
        st.caption("Version 2.6")
        st.markdown("ATS Lite resume review assistant for organizing applicant information before human review.")
        st.divider()
        st.markdown("### Outputs")
        st.markdown("- Pipeline stage\n- Review priority\n- Resume match signals\n- Missing information\n- Follow-up questions\n- Manager summary\n- Candidate email\n- PDF review packet")


def render_hero() -> None:
    st.markdown(
        """
<div class="hero"><div class="eyebrow">ATS Lite Resume Review Assistant</div><div class="hero-title">RecruitPilot AI</div><div class="hero-subtitle">Organize job descriptions and resume text into review priorities, match signals, missing information, follow-up questions, and manager-ready review packets.</div><div class="hero-pills"><span>ATS Lite</span><span>Resume Review</span><span>Pipeline Tracking</span><span>Interview Prep</span><span>Streamlit</span></div></div>
""",
        unsafe_allow_html=True,
    )


def build_inputs() -> dict | None:
    scenario_name = st.selectbox("Load Sample Scenario", list(SAMPLE_DATA.keys()))
    scenario = SAMPLE_DATA.get(scenario_name, {})
    uploaded_resume = st.file_uploader(
        "Optional: Upload resume text file (.txt or .md)",
        type=["txt", "md"],
        help=f"Plain text only. Max file size: {MAX_UPLOAD_BYTES // 1000} KB.",
    )
    uploaded_resume_text = decode_uploaded_text(uploaded_resume)

    with st.form("resume_review_form"):
        form_group("Candidate and pipeline details")
        detail_col1, detail_col2, detail_col3 = st.columns(3)
        with detail_col1:
            candidate_name = st.text_input("Candidate Name", value=scenario.get("candidate_name", ""), placeholder="Example: Jordan Miller")
        with detail_col2:
            role_title = st.text_input("Role Title", value=scenario.get("role_title", ""), placeholder="Example: Field Sales Consultant")
        with detail_col3:
            pipeline_stage = st.selectbox("Pipeline Stage", PIPELINE_STAGES, index=PIPELINE_STAGES.index(scenario.get("pipeline_stage", "Resume Review")))
        role_type = st.selectbox("Role Type", ROLE_TYPES, index=ROLE_TYPES.index(scenario.get("role_type", "Field Sales")))

        form_group("Job description and resume text")
        job_description = st.text_area("Job Description / Role Requirements", value=scenario.get("job_description", ""), height=150, max_chars=MAX_TEXT_CHARS)
        resume_text = st.text_area("Resume Text", value=uploaded_resume_text or scenario.get("resume_text", ""), height=180, max_chars=MAX_TEXT_CHARS)
        submitted = st.form_submit_button("Generate Resume Review Packet", use_container_width=True)

    if not submitted:
        return None

    job_description, job_trimmed = limit_text(job_description, MAX_TEXT_CHARS)
    resume_text, resume_trimmed = limit_text(resume_text, MAX_TEXT_CHARS)
    if job_trimmed or resume_trimmed:
        st.warning(f"Input was trimmed to {MAX_TEXT_CHARS:,} characters before analysis to keep the app reliable and cost-conscious.")

    return {
        "candidate_name": candidate_name,
        "role_title": role_title or "Open Role",
        "role_type": role_type,
        "pipeline_stage": pipeline_stage,
        "job_description": job_description,
        "resume_text": resume_text,
    }


def enhance_review(inputs: dict, workflow: dict) -> dict:
    raw_ai = enhance_text(
        build_ai_review_prompt(
            inputs["candidate_name"],
            workflow["role_title"],
            inputs["role_type"],
            inputs["pipeline_stage"],
            inputs["job_description"],
            inputs["resume_text"],
            workflow["review"],
            workflow["questions"],
            workflow["summary"],
            workflow["subject"],
            workflow["email"],
        ),
        "",
        stable_cache_key(
            "recruitpilot_review",
            {
                "candidate_name": inputs["candidate_name"],
                "role_title": workflow["role_title"],
                "job_description": inputs["job_description"],
                "resume_text": inputs["resume_text"],
            },
        ),
    )
    summary, questions, subject, email = parse_ai_review(
        raw_ai,
        workflow["summary"],
        workflow["questions"],
        workflow["subject"],
        workflow["email"],
    )
    workflow.update({"summary": summary, "questions": questions, "subject": subject, "email": email})
    return workflow


def render_results(inputs: dict, workflow: dict, pdf_packet: bytes, tracker_csv: str) -> None:
    review = workflow["review"]

    section_title("Candidate review packet preview")
    preview_col1, preview_col2, preview_col3, preview_col4 = st.columns(4)
    with preview_col1:
        metric_card("Candidate", inputs["candidate_name"] or "N/A")
    with preview_col2:
        metric_card("Stage", inputs["pipeline_stage"])
    with preview_col3:
        metric_card("Review Priority", review["priority"])
    with preview_col4:
        metric_card("Job-Term Coverage", f"{review['coverage']}%")
    html_card("Next Human Review Step", f"<p>{workflow['next_step']}</p>", "workflow-card")

    section_title("Review snapshot")
    snapshot_col1, snapshot_col2, snapshot_col3, snapshot_col4 = st.columns(4)
    with snapshot_col1:
        metric_card("Pipeline Stage", inputs["pipeline_stage"])
    with snapshot_col2:
        metric_card("Match Signals", str(review["signal_count"]))
    with snapshot_col3:
        metric_card("Missing Items", str(review["missing_count"]))
    with snapshot_col4:
        metric_card("Role Type", inputs["role_type"])

    html_card("Responsible Use Note", f"<p>{RESPONSIBLE_USE_NOTE}</p>", "warning-card")
    html_card("Review Priority Explanation", f"<p>{review['priority_note']}</p>", "output-card")

    section_title("Resume match signals and missing information")
    match_col, missing_col = st.columns(2)
    with match_col:
        html_card("Resume Match Signals", html_list(review["matched_terms"], "No clear match signals found from the provided text."), "signal-card")
    with missing_col:
        html_card("Missing / Unclear Information", html_list(review["missing_terms"], "No major missing terms identified from the provided job description."), "warning-card")

    section_title("Interview follow-up support")
    html_card("Suggested Follow-Up Questions", "<ol>" + "".join(f"<li>{question}</li>" for question in workflow["questions"]) + "</ol>", "workflow-card")

    section_title("Manager and candidate communication")
    summary_tab, email_tab = st.tabs(["Manager Summary", "Candidate Email"])
    with summary_tab:
        st.text_area("Manager-ready summary", workflow["summary"], height=260)
    with email_tab:
        st.text_input("Subject Line", workflow["subject"])
        st.text_area("Candidate email", workflow["email"], height=220)

    section_title("Downloads")
    download_col1, download_col2 = st.columns(2)
    with download_col1:
        st.download_button("Download Resume Review Packet PDF", data=pdf_packet, file_name="recruitpilot-resume-review-packet.pdf", mime="application/pdf", use_container_width=True)
    with download_col2:
        st.download_button("Download Candidate Tracker CSV Row", data=tracker_csv, file_name="recruitpilot-candidate-tracker-row.csv", mime="text/csv", use_container_width=True)


def main() -> None:
    render_sidebar()
    render_hero()

    section_title("Resume review builder", "Load a fictional sample, paste a job description and resume text, or upload a plain-text resume file. This tool supports human review and does not make employment decisions.")
    st.markdown(f'<div class="note-box">{PRIVACY_NOTE}</div>', unsafe_allow_html=True)

    inputs = build_inputs()
    if inputs is None:
        st.markdown('<div class="note-box">Paste a job description and resume text, load a sample scenario, or upload a .txt/.md resume file, then generate the review packet.</div>', unsafe_allow_html=True)
        return

    workflow = run_review_workflow(
        inputs["candidate_name"],
        inputs["role_title"],
        inputs["pipeline_stage"],
        inputs["role_type"],
        inputs["job_description"],
        inputs["resume_text"],
        RESPONSIBLE_USE_NOTE,
    )
    workflow = enhance_review(inputs, workflow)

    packet = build_review_packet(
        inputs["candidate_name"],
        workflow["role_title"],
        inputs["role_type"],
        inputs["pipeline_stage"],
        inputs["job_description"],
        inputs["resume_text"],
        workflow["review"],
        workflow["questions"],
        workflow["summary"],
        workflow["subject"],
        workflow["email"],
        workflow["next_step"],
        RESPONSIBLE_USE_NOTE,
    )
    pdf_packet = markdown_to_pdf(packet, title="RecruitPilot AI Resume Review Packet")
    tracker_csv = build_tracker_csv(inputs["candidate_name"], workflow["role_title"], inputs["pipeline_stage"], workflow["review"], workflow["next_step"])

    render_results(inputs, workflow, pdf_packet, tracker_csv)

    section_title("What this app demonstrates")
    html_card(
        "Portfolio Skills Shown",
        "<ul><li>Modular Streamlit architecture</li><li>AI-enhanced interview prep with rules-based fallback</li><li>Responsible AI workflow design</li><li>Resume and job description text parsing</li><li>Rules-based review organization</li><li>User-friendly PDF and CSV exports</li></ul>",
        "signal-card",
    )

    st.markdown(f'<div class="note-box">{PRIVACY_NOTE}</div>', unsafe_allow_html=True)


if __name__ == "__main__":
    main()
