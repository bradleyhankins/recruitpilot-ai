from core.file_parsers import extract_resume_text, extract_text_from_plain_text


def test_extract_text_from_plain_text_decodes_utf8():
    text = extract_text_from_plain_text("Resume content with CRM and sales experience".encode("utf-8"))

    assert "CRM" in text
    assert "sales" in text


def test_extract_resume_text_supports_txt_fallback():
    text, warning = extract_resume_text(
        "Candidate has sales, CRM, and customer follow-up experience.".encode("utf-8"),
        "resume.txt",
    )

    assert warning is None
    assert "customer follow-up" in text


def test_extract_resume_text_supports_md_fallback():
    text, warning = extract_resume_text(
        "# Resume\nExperience with operations and scheduling.".encode("utf-8"),
        "resume.md",
    )

    assert warning is None
    assert "operations" in text


def test_extract_resume_text_rejects_legacy_doc():
    text, warning = extract_resume_text(b"legacy doc bytes", "resume.doc")

    assert text == ""
    assert warning is not None
    assert ".doc" in warning
    assert ".docx" in warning


def test_extract_resume_text_rejects_unsupported_file_type():
    text, warning = extract_resume_text(b"spreadsheet bytes", "resume.xlsx")

    assert text == ""
    assert warning is not None
    assert "Unsupported file type" in warning
