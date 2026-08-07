from agents.document_triage_agent import triage_document
from skills.approval_logger import log_human_approval

def test_ai_triage_agent():
    # Test if the AI agent correctly flags a document for human review
    result = triage_document("test_doc.pdf", "ID_CARD")
    assert result["status"] == "PENDING_HUMAN_APPROVAL"

def test_human_audit_logger():
    # Test if the audit logger correctly captures the manager's decision
    log_output = log_human_approval("TASK-999", "Test Manager", "APPROVED")
    assert "Test Manager" in log_output
    assert "APPROVED" in log_output