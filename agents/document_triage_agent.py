# Custom Agent: Document Triage Agent

def triage_document(file_name: str, file_type: str) -> dict:
    """Processes onboarding document and prepares it for human review."""
    return {
        "file_name": file_name,
        "file_type": file_type,
        "status": "PENDING_HUMAN_APPROVAL",
        "extracted_data": {
            "employee_id": "EMP-1001",
            "document_valid": True
        }
    }