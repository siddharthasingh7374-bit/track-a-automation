from agents.ticket_triage_agent import triage_ticket
from skills.approval_logger import log_human_approval

# Create ticket
ticket_text = 'I was charged twice for my monthly subscription'

# Call triage_ticket(ticket_text)
ticket_result = triage_ticket(ticket_text)

# Print category
print(f'Classification: {ticket_result["category"]}')

# Print drafted response
print(f'Drafted Response: {ticket_result["response"]}')

# Ask user for APPROVE or REJECT
approval = input('Please type "APPROVE" or "REJECT": ')

# Call log_human_approval()
log_human_approval(approval, ticket_text, ticket_result['response'])