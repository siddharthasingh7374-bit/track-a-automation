import sys
import datetime

# Import our custom agent and skill that you created earlier
from agents.document_triage_agent import triage_document
from skills.approval_logger import log_human_approval

def main():
    print("\n=======================================================")
    print(" WELCOME TO THE AUTOMATED ONBOARDING COORDINATOR ")
    print("=======================================================\n")
    
    # Step 1: The AI Agent does its job
    print("[AI SYSTEM] Processing new employee document: 'passport.pdf'...")
    doc_result = triage_document("passport.pdf", "ID_CARD")
    print(f"[AI SYSTEM] Status: {doc_result['status']}")
    
    # Step 2: The Human-in-the-loop steps in
    print("\n--- HUMAN REVIEW REQUIRED ---")
    decision = input("Type APPROVE or REJECT for this document and press Enter: ")
    
    # Step 3: The Skill logs the action
    print("\n[SYSTEM] Saving secure audit log...")
    final_log = log_human_approval("TASK-001", "Hackathon Manager", decision.upper())
    
    print("\n=======================================================")
    print(" SUCCESS! ONBOARDING TASK COMPLETE.")
    print("=======================================================\n")

# This is the magic line that actually forces Python to start the app
if __name__ == "__main__":
    main()