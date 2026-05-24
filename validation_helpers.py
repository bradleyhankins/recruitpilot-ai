from __future__ import annotations

MAX_UPLOAD_BYTES = 500_000
MAX_RESUME_CHARS = 20_000
MAX_JOB_DESCRIPTION_CHARS = 12_000


def validate_uploaded_resume(uploaded_file) -> list[str]:
    """Return user-friendly validation errors for uploaded resume files."""
    errors: list[str] = []
    if uploaded_file is None:
        return errors

    size = getattr(uploaded_file, "size", None)
    if size is not None and size > MAX_UPLOAD_BYTES:
        errors.append("Uploaded resume text file is too large for the public demo. Please keep files under 500 KB or paste a shortened, anonymized version.")

    return errors


def trim_resume_text(text: str) -> tuple[str, list[str]]:
    warnings: list[str] = []
    if len(text) > MAX_RESUME_CHARS:
        warnings.append("Resume text was trimmed for public-demo reliability. Use a shorter, anonymized version for best results.")
        return text[:MAX_RESUME_CHARS], warnings
    return text, warnings


def trim_job_description(text: str) -> tuple[str, list[str]]:
    warnings: list[str] = []
    if len(text) > MAX_JOB_DESCRIPTION_CHARS:
        warnings.append("Job description was trimmed for public-demo reliability. Use a shorter role summary for best results.")
        return text[:MAX_JOB_DESCRIPTION_CHARS], warnings
    return text, warnings
