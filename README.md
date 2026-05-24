# RecruitPilot AI

RecruitPilot AI is a responsible ATS Lite resume review assistant for small-business and field-sales teams.

It helps hiring managers organize job descriptions and resume text into:

- Candidate pipeline stage
- Resume review priority
- Resume match signals
- Missing or unclear information
- Suggested follow-up interview questions
- Manager-ready review summaries
- Candidate follow-up emails
- Downloadable resume review packets

RecruitPilot AI is designed to support human review. It should not be used as the sole basis for selection, rejection, compensation, or employment decisions.

## Live Demo

[Launch RecruitPilot AI](https://recruitpilot-ai.streamlit.app/)

## Why this project exists

Small and mid-sized businesses often review applicants from scattered notes, pasted resumes, job descriptions, and informal conversations. RecruitPilot AI helps organize applicant information into a cleaner review packet so hiring managers can prepare better questions and document next steps more consistently.

## Who this helps

RecruitPilot AI is designed for:

- Small business owners
- Sales managers
- Field-sales teams
- Home-service companies
- Recruiting coordinators
- Operations leaders
- Hiring managers

## Current Version: v2.0

RecruitPilot AI v2.0 is positioned as an ATS Lite resume review and candidate tracking assistant.

It includes:

- Job description input
- Resume text input
- Candidate pipeline stage tracking
- Role type selector
- Resume match signal extraction
- Missing or unclear information checklist
- Review priority labels
- Follow-up interview questions
- Manager-ready review summary
- Candidate follow-up email template
- Downloadable Markdown resume review packet
- Responsible AI use note

## What it does

The app allows users to paste a job description and resume text, then generates:

- Review priority
- Pipeline stage snapshot
- Count of resume match signals
- Count of missing or unclear items
- Job-related resume signals
- Missing or unclear job terms
- Suggested follow-up questions
- Manager review summary
- Candidate follow-up email
- Downloadable review packet

## Responsible Use

RecruitPilot AI does not make hiring decisions, reject candidates, rank candidates, or replace human judgment.

The app is intended to organize information and prepare a structured review packet for a human hiring manager.

It should not be used as the sole basis for:

- Selection decisions
- Rejection decisions
- Compensation decisions
- Employment eligibility decisions
- Final hiring recommendations

## Screenshots

Screenshots will be refreshed after all portfolio apps are upgraded.

## Tech Stack

- Python
- Streamlit
- Rules-based workflow logic
- Markdown report export
- GitHub
- Streamlit Community Cloud

## Portfolio Purpose

This project was built as part of Bradley Hankins' AI operations and workflow automation portfolio.

RecruitPilot AI demonstrates how practical AI-assisted tools can help small and mid-sized businesses organize resume review, applicant tracking context, interview preparation, manager documentation, and candidate communication while keeping humans responsible for employment decisions.

## Run Locally

```bash
py -m pip install -r requirements.txt
py -m streamlit run app.py
```

## Built By

Bradley Hankins  
Operations & Revenue Leader | AI Workflow Automation | RevOps & Process Improvement

## Case Study

### Problem

Small and mid-sized businesses often review applicants using scattered notes, resumes, job descriptions, and informal interview impressions. This can make it difficult to identify relevant resume signals, spot missing information, prepare follow-up questions, and document the review process consistently.

Common issues include:

- Resume review notes scattered across systems
- Job requirements not clearly compared against resume text
- Missing information not documented before interviews
- Follow-up questions created from memory instead of a structured process
- Candidate communication written manually each time
- Little consistency in applicant review packets

### Solution

RecruitPilot AI was rebuilt as a responsible ATS Lite resume review assistant.

The app allows a user to paste a job description and resume text, select a role type and pipeline stage, then generate a structured review packet that organizes resume match signals, missing information, interview questions, manager summaries, and candidate communication.

### My Role

I designed and built this project from concept to deployment, including:

- Defining the recruiting workflow problem
- Reframing the app for responsible human review
- Designing the resume review workflow
- Building the Streamlit app
- Writing rules-based keyword and signal extraction logic
- Creating review priority labels
- Creating manager-ready summaries
- Creating candidate follow-up email templates
- Building downloadable Markdown review packets
- Preparing fictional sample scenarios for public portfolio use
- Publishing the project on GitHub
- Deploying the live demo

### Business Value

RecruitPilot AI helps small and mid-sized businesses organize applicant review more consistently without replacing human judgment.

The tool can help teams:

- Review job descriptions and resumes in one workflow
- Identify resume signals related to the role
- Document missing or unclear information
- Prepare better follow-up interview questions
- Create manager-ready review summaries
- Standardize candidate communication
- Produce downloadable review documentation
- Improve applicant tracking discipline

### Future Improvements

Planned future improvements include:

- File upload for resumes
- Job description templates
- Multi-candidate tracking dashboard
- CSV export for candidate pipeline records
- PDF report downloads
- Optional OpenAI API integration for dynamic summaries
- Interview scorecard exports
- Recruiting pipeline analytics
