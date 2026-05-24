# Development Notes

## Build Philosophy

RecruitPilot AI is designed as a responsible ATS Lite workflow assistant.

The goal is to organize applicant information for human review, not to automate hiring decisions.

## Engineering Priorities

1. Responsible AI positioning
2. Human-review workflow support
3. Transparent rules-based review logic
4. Clear review packet generation
5. Public-safe fictional sample data
6. Simple deployment on Streamlit Community Cloud

## Current Tradeoffs

The current portfolio version keeps all deployment logic in `app.py` for easy review and deployment.

A future production version should split role configuration, review logic, and export generation into separate modules.

## Future Refactor Plan

A future production-oriented version should split the app into:

```text
src/config.py
src/resume_review.py
src/responsible_use.py
src/reports.py
src/exports.py
src/components.py
src/styles.css
```

## Testing Opportunities

The most valuable future tests would cover:

- Job-term extraction
- Resume match signal detection
- Missing information detection
- Review priority labels
- Next human review step logic
- Candidate tracker CSV export
- Markdown packet generation

## Code Quality Roadmap

Potential future tooling:

- Ruff for linting and formatting
- Pytest for review logic tests
- Pre-commit hooks
- GitHub Actions smoke checks

## Responsible AI Notes

RecruitPilot should continue avoiding:

- Automated hiring decisions
- Candidate rejection recommendations
- Candidate ranking
- Protected-class inference
- Final employment recommendations
