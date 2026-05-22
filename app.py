import streamlit as st

st.set_page_config(page_title="RecruitPilot AI", page_icon="🧑‍💼", layout="wide")

def score_candidate(sales_experience, industry_experience, prospecting_comfort, crm_experience, compensation_alignment, availability, communication_rating, coachability_rating, reliability_rating):
    score = 0
    score += {"5+ years": 20, "2-5 years": 16, "6-24 months": 10, "No direct sales experience": 4}.get(sales_experience, 0)
    score += {"Same industry": 15, "Related home-service industry": 12, "Other sales industry": 8, "No relevant industry experience": 3}.get(industry_experience, 0)
    score += {"High": 15, "Medium": 9, "Low": 3, "Not Comfortable": 0}.get(prospecting_comfort, 0)
    score += {"Strong": 12, "Some": 8, "Limited": 4, "None": 0}.get(crm_experience, 0)
    score += {"Aligned": 12, "Needs Discussion": 6, "Not Aligned": 1}.get(compensation_alignment, 0)
    score += {"Immediate": 8, "Within 2 weeks": 6, "30+ days": 2}.get(availability, 0)
    score += communication_rating * 2.5
    score += coachability_rating * 2.5
    score += reliability_rating * 2

    score = min(round(score), 100)

    if score >= 82:
        return score, "Strong Candidate", "Move forward quickly and schedule final interview or offer conversation."
    if score >= 68:
        return score, "Qualified Candidate", "Move forward, but use follow-up questions to confirm fit."
    if score >= 52:
        return score, "Possible Fit", "Keep in consideration, but compare against stronger candidates."
    return score, "Not Recommended Yet", "Do not advance unless there is a strong reason outside the current information."

def risk_level(score, red_count):
    if score < 52 or red_count >= 4:
        return "High Risk", "Candidate has multiple concerns or a low fit score. Proceed carefully."
    if score < 68 or red_count >= 2:
        return "Moderate Risk", "Candidate may be viable, but key concerns should be validated before advancing."
    return "Low Risk", "Candidate appears to be a relatively clean fit based on the current inputs."

def success_profile(role):
    profiles = {
        "Field Sales Representative": [
            "Comfortable with proactive prospecting and rejection",
            "Strong follow-up discipline",
            "Able to explain value clearly to customers",
            "Coachability and daily activity consistency",
            "Reliable CRM documentation"
        ],
        "Sales Consultant": [
            "Strong discovery and presentation skills",
            "Comfort discussing price and value",
            "Consistent follow-up habits",
            "Ability to build trust quickly",
            "Strong communication and process discipline"
        ],
        "Project Consultant": [
            "Ability to balance customer communication and project detail",
            "Good documentation habits",
            "Strong handoff communication",
            "Problem-solving mindset",
            "Comfort working between sales and operations"
        ],
        "Sales Manager": [
            "Ability to coach reps and inspect pipeline activity",
            "Strong accountability habits",
            "Data-driven decision-making",
            "Recruiting and onboarding capability",
            "Consistent meeting and performance cadence"
        ],
        "Operations Coordinator": [
            "Strong organizational skills",
            "Detail-oriented communication",
            "Reliable process follow-through",
            "Comfort using systems and documentation",
            "Ability to support multiple stakeholders"
        ],
        "Customer Success Representative": [
            "Strong communication and empathy",
            "Follow-up consistency",
            "Problem resolution mindset",
            "CRM note discipline",
            "Ability to protect customer experience"
        ],
        "Other": [
            "Clear role expectations",
            "Communication strength",
            "Process discipline",
            "Coachability",
            "Reliable follow-through"
        ]
    }
    return profiles.get(role, profiles["Other"])

def green_flags(sales_experience, industry_experience, prospecting_comfort, crm_experience, communication_rating, coachability_rating, reliability_rating):
    flags = []
    if sales_experience in ["2-5 years", "5+ years"]:
        flags.append("Relevant sales experience that may reduce ramp-up time.")
    if industry_experience in ["Same industry", "Related home-service industry"]:
        flags.append("Industry familiarity that may help with customer conversations and field expectations.")
    if prospecting_comfort == "High":
        flags.append("Comfortable with proactive prospecting and self-generated activity.")
    if crm_experience in ["Strong", "Some"]:
        flags.append("Has enough CRM exposure to support clean pipeline and follow-up discipline.")
    if communication_rating >= 4:
        flags.append("Strong communication rating based on interview inputs.")
    if coachability_rating >= 4:
        flags.append("Strong coachability rating, which supports training adoption.")
    if reliability_rating >= 4:
        flags.append("Strong reliability rating, which supports role consistency and accountability.")
    return flags or ["No major green flags identified from the current inputs."]

def red_flags(sales_experience, prospecting_comfort, crm_experience, compensation_alignment, availability, communication_rating, coachability_rating, reliability_rating):
    flags = []
    if sales_experience == "No direct sales experience":
        flags.append("Limited direct sales experience may require a longer ramp-up period.")
    if prospecting_comfort in ["Low", "Not Comfortable"]:
        flags.append("Low comfort with proactive prospecting may limit success in field-sales roles.")
    if crm_experience == "None":
        flags.append("No CRM experience could create follow-up and documentation challenges.")
    if compensation_alignment == "Not Aligned":
        flags.append("Compensation expectations may not match the role structure.")
    if availability == "30+ days":
        flags.append("Delayed availability may create hiring timing issues.")
    if communication_rating <= 2:
        flags.append("Communication rating is low and may affect customer-facing performance.")
    if coachability_rating <= 2:
        flags.append("Coachability rating is low and may affect training adoption.")
    if reliability_rating <= 2:
        flags.append("Reliability rating is low and may create attendance, follow-through, or accountability concerns.")
    return flags or ["No major red flags identified from the current inputs."]

def interview_questions(role, sales_experience, prospecting_comfort, compensation_alignment, crm_experience, red_list):
    questions = [
        f"What interests you most about the {role} role?",
        "Walk me through how you normally follow up with a prospect after a sales conversation.",
        "Tell me about a time you had to handle rejection or a difficult customer.",
        "How do you stay organized with leads, appointments, notes, and follow-up tasks?"
    ]

    if sales_experience in ["No direct sales experience", "6-24 months"]:
        questions.append("What makes you confident you can succeed in a performance-driven environment?")
    else:
        questions.append("What sales process or habits have helped you succeed in previous roles?")

    if prospecting_comfort != "High":
        questions.append("How comfortable are you initiating conversations with prospects who were not expecting you?")

    if compensation_alignment != "Aligned":
        questions.append("What income range are you targeting, and how do you feel about performance-based compensation?")

    if crm_experience in ["Limited", "None"]:
        questions.append("What systems or routines would you use to make sure your notes, follow-ups, and pipeline stay clean?")

    if red_list and "No major red flags identified from the current inputs." not in red_list:
        questions.append("What would your previous manager say is the biggest area you still need to improve?")

    return questions

def interview_scorecard(role):
    profile = success_profile(role)
    rows = []
    for item in profile:
        rows.append({"Competency": item, "Suggested Rating": "1-5", "Evidence to Listen For": "Specific examples, clear ownership, and repeatable habits"})
    return rows

def candidate_email(candidate_name, role, recommendation):
    name = candidate_name or "there"
    if recommendation in ["Strong Candidate", "Qualified Candidate"]:
        subject = f"Next Step for the {role} Opportunity"
        body = f"""Hi {name},

Thank you again for taking the time to speak with us about the {role} opportunity.

We enjoyed learning more about your background and would like to continue the conversation. The next step would be to schedule a follow-up discussion so we can go deeper into the role, expectations, and what success looks like.

Please let me know what times work best for you.

Thanks again,
Hiring Team"""
    elif recommendation == "Possible Fit":
        subject = f"Following Up on the {role} Opportunity"
        body = f"""Hi {name},

Thank you again for your interest in the {role} opportunity.

We are continuing to review candidates and wanted to keep the conversation open. We may have a few additional questions to better understand fit for the role and next steps.

Thank you again for your time,
Hiring Team"""
    else:
        subject = f"Update on the {role} Opportunity"
        body = f"""Hi {name},

Thank you for taking the time to speak with us about the {role} opportunity.

At this time, we are continuing with candidates who more closely align with the current needs of the role. We appreciate your interest and wish you the best in your search.

Thank you,
Hiring Team"""
    return subject, body

def onboarding_plan(role, recommendation, red_list):
    if recommendation not in ["Strong Candidate", "Qualified Candidate"]:
        return "Onboarding plan not recommended until candidate fit is confirmed."

    focus = "General onboarding focus: sales process, CRM discipline, communication standards, and daily activity expectations."
    if red_list and "No major red flags identified from the current inputs." not in red_list:
        focus = "Onboarding should specifically address the review areas identified during screening."

    return f"""Primary Onboarding Focus:
{focus}

Day 1:
- Company overview
- Role expectations
- CRM login/setup
- Review activity standards and communication expectations

Week 1:
- Shadow experienced team member
- Learn lead intake and follow-up workflow
- Practice discovery, objection handling, and CRM notes
- Review daily reporting expectations

Weeks 2-4:
- Begin controlled customer interactions
- Review pipeline with manager daily
- Complete roleplay scenarios
- Track activity, follow-up, and conversion metrics

30-Day Success Check:
- Review activity level
- Review CRM discipline
- Review communication quality
- Review coachability and process adoption
- Confirm whether the candidate is trending toward success in the {role} role
"""

# -----------------------------
# Header
# -----------------------------

st.title("🧑‍💼 RecruitPilot AI")
st.subheader("AI-assisted candidate screening workflow tool for field-sales and small-business teams")

st.markdown("""
RecruitPilot AI helps hiring managers turn interview notes and candidate details into fit scores,
risk levels, green flags, red flags, follow-up questions, hiring recommendations, candidate emails,
onboarding plans, and downloadable candidate review reports.
""")

st.sidebar.title("RecruitPilot AI")
st.sidebar.caption("Version 1.1 MVP")
st.sidebar.markdown("""
**Built by Bradley Hankins**

A practical AI workflow automation tool for recruiting, candidate screening, and hiring decision support.
""")
st.sidebar.divider()

with st.sidebar.expander("What this app generates"):
    st.markdown("""
    - Candidate fit score
    - Risk level
    - Hiring recommendation
    - Success profile
    - Green flags
    - Red flags
    - Follow-up interview questions
    - Interview scorecard
    - Candidate email
    - Onboarding plan
    - Downloadable report
    """)

# -----------------------------
# Candidate Form
# -----------------------------

st.header("Candidate Screening Builder")

with st.form("candidate_form"):
    col1, col2 = st.columns(2)

    with col1:
        candidate_name = st.text_input("Candidate Name", placeholder="Example: Jordan Miller")
        role = st.selectbox("Role Applied For", ["Field Sales Representative", "Sales Consultant", "Project Consultant", "Sales Manager", "Operations Coordinator", "Customer Success Representative", "Other"])
        sales_experience = st.selectbox("Sales Experience", ["No direct sales experience", "6-24 months", "2-5 years", "5+ years"])
        industry_experience = st.selectbox("Industry Experience", ["Same industry", "Related home-service industry", "Other sales industry", "No relevant industry experience"])
        prospecting_comfort = st.selectbox("Comfort With Proactive Prospecting", ["High", "Medium", "Low", "Not Comfortable"])

    with col2:
        crm_experience = st.selectbox("CRM Experience", ["Strong", "Some", "Limited", "None"])
        compensation_alignment = st.selectbox("Compensation Expectations", ["Aligned", "Needs Discussion", "Not Aligned"])
        availability = st.selectbox("Availability", ["Immediate", "Within 2 weeks", "30+ days"])
        communication_rating = st.slider("Communication Rating", 1, 5, 3)
        coachability_rating = st.slider("Coachability Rating", 1, 5, 3)
        reliability_rating = st.slider("Reliability / Follow-Through Rating", 1, 5, 3)

    interview_notes = st.text_area("Interview Notes", placeholder="Example: Candidate has strong customer-facing experience, wants growth opportunity, and is open to performance-based compensation.")

    submitted = st.form_submit_button("Generate Candidate Review")

if submitted:
    score, recommendation, next_step = score_candidate(
        sales_experience, industry_experience, prospecting_comfort, crm_experience,
        compensation_alignment, availability, communication_rating, coachability_rating, reliability_rating
    )

    greens = green_flags(sales_experience, industry_experience, prospecting_comfort, crm_experience, communication_rating, coachability_rating, reliability_rating)
    reds = red_flags(sales_experience, prospecting_comfort, crm_experience, compensation_alignment, availability, communication_rating, coachability_rating, reliability_rating)
    risk, risk_note = risk_level(score, len([r for r in reds if "No major red flags" not in r]))
    questions = interview_questions(role, sales_experience, prospecting_comfort, compensation_alignment, crm_experience, reds)
    scorecard = interview_scorecard(role)
    email_subject, email_body = candidate_email(candidate_name, role, recommendation)
    plan = onboarding_plan(role, recommendation, reds)
    profile = success_profile(role)

    manager_note = f"""{candidate_name or "Candidate"} is being evaluated for the {role} role.

Fit Score: {score}/100
Recommendation: {recommendation}
Risk Level: {risk}

Summary:
The candidate shows the following strengths:
- {"; ".join(greens)}

Areas to review:
- {"; ".join(reds)}

Recommended Next Step:
{next_step}
"""

    st.divider()
    st.header("Candidate Review")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Fit Score", f"{score}/100")
    col2.metric("Recommendation", recommendation)
    col3.metric("Risk Level", risk)
    col4.metric("Next Step", "Review below")

    st.info(risk_note)

    st.subheader("Role Success Profile")
    for item in profile:
        st.markdown(f"- {item}")

    st.subheader("Green Flags")
    for flag in greens:
        st.success(flag)

    st.subheader("Red Flags / Review Areas")
    for flag in reds:
        st.warning(flag)

    st.subheader("Suggested Follow-Up Interview Questions")
    for i, question in enumerate(questions, start=1):
        st.markdown(f"{i}. {question}")

    st.subheader("Interview Scorecard")
    st.table(scorecard)

    st.subheader("Internal Manager Note")
    st.text_area("Manager-ready summary", manager_note, height=260)

    st.subheader("Candidate Follow-Up Email")
    st.text_input("Subject Line", email_subject)
    st.text_area("Email Body", email_body, height=260)

    st.subheader("Recommended Onboarding Plan")
    st.text_area("Onboarding plan", plan, height=340)

    report = f"""# RecruitPilot AI Candidate Review

## Candidate

Candidate: {candidate_name or "N/A"}  
Role Applied For: {role}  
Fit Score: {score}/100  
Recommendation: {recommendation}  
Risk Level: {risk}  
Next Step: {next_step}  

## Candidate Inputs

Sales Experience: {sales_experience}  
Industry Experience: {industry_experience}  
Prospecting Comfort: {prospecting_comfort}  
CRM Experience: {crm_experience}  
Compensation Alignment: {compensation_alignment}  
Availability: {availability}  
Communication Rating: {communication_rating}/5  
Coachability Rating: {coachability_rating}/5  
Reliability Rating: {reliability_rating}/5  

## Interview Notes

{interview_notes or "No notes provided."}

## Role Success Profile

""" + "\n".join([f"- {item}" for item in profile]) + """

## Green Flags

""" + "\n".join([f"- {flag}" for flag in greens]) + """

## Red Flags / Review Areas

""" + "\n".join([f"- {flag}" for flag in reds]) + """

## Suggested Follow-Up Interview Questions

""" + "\n".join([f"{i}. {question}" for i, question in enumerate(questions, start=1)]) + f"""

## Internal Manager Note

{manager_note}

## Candidate Follow-Up Email

Subject: {email_subject}

{email_body}

## Recommended Onboarding Plan

{plan}

---

Generated by RecruitPilot AI.
"""

    st.download_button("Download Candidate Review Report", data=report, file_name="recruitpilot-candidate-review.md", mime="text/markdown")
else:
    st.info("Complete the form and click Generate Candidate Review to create screening insights, interview questions, and hiring recommendations.")

st.divider()

st.header("Built for Practical AI Recruiting Operations")
st.markdown("""
RecruitPilot AI is a portfolio project demonstrating how AI-assisted workflows can help small businesses
standardize candidate evaluation, improve interview consistency, document hiring decisions, and prepare
basic onboarding plans without needing enterprise HR software.

This MVP uses rules-based logic to keep the app free, simple, and easy to deploy. Future versions can include
OpenAI API integration, job-description matching, resume parsing, interview scorecards, and team-level recruiting analytics.
""")
st.info("Privacy note: Information entered into this app is processed during the active session and is not saved by this app.")
