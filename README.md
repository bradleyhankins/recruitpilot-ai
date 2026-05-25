# RecruitPilot AI

RecruitPilot AI is a responsible, AI-enhanced ATS Lite resume review assistant for small-business and field-sales teams. It organizes job descriptions and resume files into structured human-review packets, interview prep, candidate communication, and applicant tracking exports.

RecruitPilot AI is designed to support human review. It should not be used as the sole basis for selection, rejection, compensation, or employment decisions.

## Live Demo

[Launch RecruitPilot AI](https://recruitpilot-ai.streamlit.app/)

## Current Version: v2.7

RecruitPilot AI combines a deterministic rules-based review organizer with embedded AI-enhanced interview preparation support.

The app is designed to work in two layers:

1. **Rules-based core:** extracts job-related terms, identifies resume match signals, highlights missing or unclear information, creates follow-up questions, and builds a structured human-review packet.
2. **Embedded AI layer:** when an OpenAI token is available, the app quietly improves the manager summary, follow-up questions, and candidate email while preserving responsible-use guardrails.

If the AI call fails or an API key is unavailable, the app silently falls back to the rules-based review packet. The user experience stays the same.

## Architecture

RecruitPilot has been refactored from a single-file Streamlit prototype into a modular application.

```text
recruitpilot-ai/
├── app.py
├── ai_helpers.py
├── pdf_helpers.py
├── requirements.txt
├── core/
│   ├── __init__.py
│   ├── file_parsers.py
│   ├── prompts.py
│   ├── report_builder.py
│   └── review_logic.py
├── data/
│   ├── __init__.py
│   └── sample_data.py
└── tests/
    ├── test_file_parsers.py
    └── test_review_logic.py
```

### Module Responsibilities

- `app.py` handles Streamlit layout, form inputs, upload handling, rendering, and orchestration.
- `core/file_parsers.py` extracts resume text from PDF, DOCX, TXT, and MD files.
- `core/review_logic.py` contains job-term extraction, resume signal review, follow-up question logic, human next-step logic, and workflow orchestration.
- `core/prompts.py` contains responsible AI prompt construction and structured AI output parsing.
- `core/report_builder.py` builds the PDF review packet content and candidate tracker CSV row.
- `data/sample_data.py` stores sample scenarios, role types, pipeline stages, keyword libraries, upload limits, and responsible-use notes.
- `ai_helpers.py` manages OpenAI access, guardrails, prompt length control, stable cache keys, and silent fallback behavior.
- `pdf_helpers.py` converts structured report text into a downloadable PDF.

## Resume Upload Support

RecruitPilot supports common resume formats:

- PDF
- DOCX
- TXT fallback
- MD fallback

Legacy `.doc` files are not supported in this public demo. Users should save legacy Word documents as `.docx` or PDF before uploading.

For scanned or image-based PDFs, the app may not find readable text. In that case, the user can paste the resume text manually or upload a text-based PDF/DOCX.

## AI Design Pattern

The guiding principle is:

```text
Rules decide. AI polishes. Guardrails constrain. Fallback protects.
```

The rules-based workflow remains the source of truth for:

- Review priority
- Job-term coverage
- Match signals
- Missing or unclear information
- Next human review step
- Responsible-use note
- Candidate tracker CSV row

The AI layer is used only to improve the clarity and usefulness of interview preparation, manager summaries, and candidate communication. It must not rank candidates, make selection/rejection decisions, infer protected characteristics, or replace human judgment.

## Responsible Use

RecruitPilot AI does not make hiring decisions, reject candidates, rank candidates, or replace human judgment.

The app is intended to organize information and prepare a structured review packet for a human hiring manager.

It should not be used as the sole basis for:

- Selection decisions
- Rejection decisions
- Compensation decisions
- Employment eligibility decisions
- Final hiring recommendations

## Privacy and Data Handling

This public demo is designed for fictional or sample data.

Users should not upload sensitive, confidential, regulated, or unnecessary personal information. When AI enhancement is enabled, entered text and extracted resume text may be processed by the configured AI provider for output enhancement.

## Why this project exists

Small and mid-sized businesses often review applicants from scattered notes, pasted resumes, job descriptions, and informal conversations. RecruitPilot AI helps organize applicant information into a cleaner review packet so hiring managers can prepare better questions and document next steps more consistently.

## Workflow Outputs

- Candidate and role details
- Pipeline stage tracking
- Role type selector
- PDF/DOCX resume upload support
- Resume text extraction
- Job description input
- Resume text input/paste fallback
- Resume match signal extraction
- Job-term coverage calculation
- Missing or unclear information checklist
- Review priority labels
- Next human review step
- AI-enhanced follow-up interview questions with rules-based fallback
- AI-enhanced manager-ready review summary with rules-based fallback
- AI-enhanced candidate follow-up email with rules-based fallback
- Downloadable PDF resume review packet
- Candidate tracker CSV row export

## Export Strategy

Current user-facing exports:

- PDF resume review packet for hiring manager review
- Candidate tracker CSV row for applicant tracking workflows

The app no longer exposes Markdown as the primary user-facing download because non-technical users expect a polished PDF report.

## Suggested Test Flow

1. Launch the live demo.
2. Load the “Field Sales Resume Review” sample scenario.
3. Optionally upload a PDF or DOCX resume.
4. Generate the resume review packet.
5. Review the pipeline stage, review priority, match signals, and job-term coverage.
6. Review missing or unclear information and AI-enhanced follow-up interview questions.
7. Review the manager summary and candidate email.
8. Download the PDF resume review packet and candidate tracker CSV row.

## Automated Tests

This repo includes unit tests for the deterministic review logic and resume parser helpers.

Run tests locally with:

```bash
py -m pip install -r requirements.txt
py -m pip install pytest
py -m pytest
```

GitHub Actions runs the test suite automatically on push and pull request events.

## Screenshots

Screenshots will be refreshed after the final UI and PDF polish pass.

## Tech Stack

- Python
- Streamlit
- OpenAI API integration
- Responsible AI workflow design
- Rules-based review organization
- Modular app architecture
- Silent AI fallback pattern
- AI guardrails
- PDF resume parsing with `pypdf`
- DOCX resume parsing with `python-docx`
- PDF report export
- CSV export
- Pytest
- GitHub Actions
- GitHub
- Streamlit Community Cloud

## Run Locally

```bash
py -m pip install -r requirements.txt
py -m streamlit run app.py
```

## Environment Variables

To enable embedded AI output:

```bash
OPENAI_TOKEN=your_api_key_here
```

The app still works without this token by using the rules-based fallback.

## Public Demo Note

All sample data, names, companies, and scenarios used in this project are fictional and created for public portfolio demonstration purposes.

## Case Study

### Problem

Small and mid-sized businesses often review applicants using scattered notes, resumes, job descriptions, and informal interview impressions. This can make it difficult to identify relevant resume signals, spot missing information, prepare follow-up questions, and document the review process consistently.

### Solution

RecruitPilot AI organizes job descriptions and resume text into a structured review packet that supports human review. The embedded AI layer improves interview preparation, manager summaries, and candidate communication while preserving strict responsible-use boundaries.

### Business Value

RecruitPilot AI helps small and mid-sized businesses organize applicant review more consistently without replacing human judgment.

## Built By

Bradley Hankins  
Operations & Revenue Leader | AI Workflow Automation | RevOps & Process Improvement

<!-- CI rerun marker: test expectation fixed -->
