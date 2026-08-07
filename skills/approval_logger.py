# Custom Skill: Human Approval Logger
import datetime

def log_human_approval(task_id: str, manager_name: str, decision: str) -> str:
    """Logs human approval/rejection decisions for traceability."""
    timestamp = datetime.datetime.now().isoformat()
    log_entry = f"[{timestamp}] Task {task_id} - Approved by: {manager_name} - Decision: {decision}"
    print(f"AUDIT LOG: {log_entry}")
    return log_entry