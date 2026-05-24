# Architecture

RecruitPilot AI is a responsible ATS Lite resume review assistant for small-business and field-sales teams.

## Current Architecture

The current version is optimized for simple Streamlit Community Cloud deployment and transparent GitHub review.

```text
app.py
README.md
requirements.txt
screenshots/
```

## Application Layers

The app is currently deployed from one Streamlit entrypoint, but the code is organized conceptually into clear layers:

```text
Configuration
- Pipeline stages
- Role types
- Sample scenarios
- Keyword libraries
- Responsible-use language

Resume Review Logic
- Text tokenization
- Job-term extraction
- Resume signal matching
- Missing information detection
- Job-term coverage calculation
- Review priority logic
- Next human review step logic

Output Generation
- Manager summary generation
- Candidate email generation
- Resume review packet generation
- Candidate tracker CSV export

Presentation
- Streamlit builder form
- Candidate packet preview
- Review snapshot cards
- Match signal cards
- Communication tabs
- Download buttons
```

## Responsible AI Design

RecruitPilot intentionally avoids automated hiring decisions, rejection decisions, ranking, or employment recommendations.

The app is designed to organize applicant information for human review only.

## Design Choices

Key design goals:

- Keep human judgment central
- Make review logic transparent
- Avoid protected-class inference
- Use public-safe fictional sample data
- Generate manager-ready documentation
- Support lightweight ATS-style tracking exports

## Why Single-File for This Version

The portfolio version keeps the deployed app easy to inspect and run. For a production application, the review logic and report generation would be split into modules.

## Future Production Layout

```text
app.py
src/
  config.py
  resume_review.py
  responsible_use.py
  reports.py
  exports.py
  components.py
  styles.css
tests/
  test_resume_review.py
  test_exports.py
```

## Future Refactor Plan

1. Move CSS into `styles.css`
2. Move role and keyword configuration into `src/config.py`
3. Move review logic into `src/resume_review.py`
4. Move Markdown and CSV exports into `src/reports.py` and `src/exports.py`
5. Add tests for review priority and CSV export generation
6. Add documentation around responsible AI limitations
