import streamlit as st

from ai_helpers import generate_ai_text

st.set_page_config(page_title="RecruitPilot AI - AI Interview Prep", page_icon="🧑‍💼", layout="wide")

st.title("AI Interview Prep Assistant")
st.caption("Optional AI enhancement for generating human-review interview questions and clarification notes.")

st.warning(
    "Responsible use: This page supports human interview preparation only. It does not rank, reject, select, or recommend hiring decisions."
)
st.info(
    "This page is optional. The main RecruitPilot workflow still works without AI. "
    "Set OPENAI_TOKEN in the deployment environment to enable AI output."
)

role_description = st.text_area(
    "Role description / requirements",
    height=180,
    placeholder="Paste the role description or key requirements.",
)
resume_notes = st.text_area(
    "Resume notes / review packet findings",
    height=220,
    placeholder="Paste resume text, match signals, missing information, or notes from RecruitPilot.",
)
prep_focus = st.selectbox(
    "Interview prep focus",
    ["Clarification questions", "Phone screen guide", "Manager interview guide", "Missing information review", "Candidate communication"],
)

if st.button("Generate AI Interview Prep", use_container_width=True):
    prompt = f"""
You are an interview preparation assistant for human hiring managers.
Support human review only. Do not rank, reject, select, or recommend whether to hire the person.
Generate practical interview preparation based on the role and resume notes.
Do not infer protected characteristics.

Prep focus: {prep_focus}

Role description / requirements:
{role_description}

Resume notes / review findings:
{resume_notes}

Return:
1. Neutral candidate summary for human review
2. Clarification areas
3. Interview questions tied to job requirements
4. Follow-up questions for missing information
5. Suggested notes for the hiring manager
6. Responsible-use reminder
"""
    with st.spinner("Generating AI interview prep..."):
        st.markdown(generate_ai_text(prompt))

st.divider()
st.markdown(
    "**AI positioning:** This page adds an interview-preparation layer while keeping employment decisions with human reviewers."
)
