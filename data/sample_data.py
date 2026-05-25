PIPELINE_STAGES = ["New Applicant", "Resume Review", "Phone Screen", "Interview Scheduled", "Interview Completed", "Reference Check", "Human Decision Pending"]
ROLE_TYPES = ["Field Sales", "Inside Sales", "Operations", "Customer Success", "Project Management", "General Business"]
MAX_UPLOAD_BYTES = 750_000
MAX_TEXT_CHARS = 12000

SAMPLE_DATA = {
    "Blank / Custom": {},
    "Field Sales Resume Review": {
        "candidate_name": "Jordan Miller",
        "role_title": "Field Sales Consultant",
        "role_type": "Field Sales",
        "pipeline_stage": "Resume Review",
        "job_description": "We are looking for a field sales consultant with customer-facing sales experience, strong follow-up habits, CRM usage, comfort with prospecting, appointment setting, and the ability to explain value clearly to homeowners.",
        "resume_text": "Jordan Miller has 4 years of customer-facing sales experience in home services. Experience includes appointment setting, CRM updates, outbound follow-up, lead tracking, customer presentations, and working with homeowners to explain project options.",
    },
    "Operations Resume Review": {
        "candidate_name": "Morgan Ellis",
        "role_title": "Operations Coordinator",
        "role_type": "Operations",
        "pipeline_stage": "Resume Review",
        "job_description": "Seeking an operations coordinator with strong organization, scheduling, CRM or spreadsheet experience, documentation habits, customer communication, and process follow-through.",
        "resume_text": "Morgan Ellis has experience coordinating schedules, managing spreadsheets, updating CRM records, documenting customer notes, and supporting office workflows. Strong organization and communication skills.",
    },
}

KEYWORD_LIBRARY = {
    "Field Sales": ["sales", "prospecting", "follow-up", "crm", "appointment", "customer", "presentation", "closing", "lead", "outbound", "homeowner"],
    "Inside Sales": ["sales", "phone", "email", "crm", "lead", "appointment", "follow-up", "customer", "pipeline", "inbound", "outbound"],
    "Operations": ["operations", "scheduling", "spreadsheet", "crm", "documentation", "process", "coordination", "customer", "office", "workflow"],
    "Customer Success": ["customer", "service", "support", "retention", "follow-up", "communication", "issue", "crm", "experience", "resolution"],
    "Project Management": ["project", "schedule", "coordination", "customer", "vendor", "timeline", "documentation", "scope", "quality", "communication"],
    "General Business": ["customer", "communication", "organization", "crm", "process", "follow-up", "team", "documentation", "sales", "operations"],
}

RESPONSIBLE_USE_NOTE = "This tool organizes resume information for human review. It should not be used as the sole basis for selection, rejection, compensation, or employment decisions."
PRIVACY_NOTE = "Privacy note: Use fictional/sample data for public demos. Do not upload sensitive, confidential, regulated, or unnecessary personal information. If AI is enabled, the entered text may be processed by the configured AI provider for output enhancement."
