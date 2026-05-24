# Project Structure

```text
.
├── app.py                  # Streamlit application entrypoint
├── README.md               # Project overview, responsible use note, and case study
├── ARCHITECTURE.md         # Architecture and responsible AI design decisions
├── PROJECT_STRUCTURE.md    # Repository structure reference
├── DEVELOPMENT_NOTES.md    # Implementation notes and future refactor plan
├── requirements.txt        # Python dependencies
└── screenshots/            # README screenshots
```

## Current File Responsibilities

### `app.py`

Contains the deployed Streamlit ATS Lite workflow.

Responsibilities:

- Page configuration
- Sample scenarios
- Role and keyword configuration
- Resume text review logic
- Missing information detection
- Review packet generation
- Candidate tracker CSV export
- Responsible-use messaging
- Streamlit UI rendering

## Future Production Structure

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

The current structure prioritizes clear portfolio review and simple deployment while documenting a responsible path toward a more modular production build.
