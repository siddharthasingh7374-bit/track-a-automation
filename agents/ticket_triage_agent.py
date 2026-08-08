def triage_ticket(ticket_text):
    """Classify a support ticket and draft a response.
    
    The agent only recommends. Human approval is required before action.
    """
    text = ticket_text.lower()

    # Classify ticket
    if any(word in text for word in [
        "charged", "charge", "payment", "refund", "invoice", "billing"
    ]):
        category = "Billing"
        team = "Billing Team"
        response = (
            "Thanks for contacting us. We understand your billing concern "
            "and will review the charge and help resolve it promptly."
        )
    elif any(word in text for word in [
        "error", "bug", "crash", "not working", "technical", "login issue"
    ]):
        category = "Technical Support"
        team = "Technical Support Team"
        response = (
            "Thanks for reporting this issue. Our technical support team "
            "will investigate the problem and help you get back up and running."
        )
    elif any(word in text for word in [
        "password", "account", "profile", "username"
    ]):
        category = "Account"
        team = "Account Team"
        response = (
            "Thanks for reaching out about your account. Our account team "
            "will review your request and help you resolve it."
        )
    else:
        category = "General"
        team = "Customer Support Team"
        response = (
            "Thanks for contacting us. Our customer support team will "
            "review your request and get back to you shortly."
        )

    # Determine priority
    if any(word in text for word in [
        "urgent", "critical", "unable", "security"
    ]):
        priority = "High"
    else:
        priority = "Medium"

    # Determine sentiment
    if any(word in text for word in [
        "angry", "frustrated", "terrible", "unacceptable"
    ]):
        sentiment = "Negative"
    else:
        sentiment = "Neutral"

    return {
        "category": category,
        "priority": priority,
        "team": team,
        "sentiment": sentiment,
        "response": response,
        "status": "PENDING_HUMAN_APPROVAL",
    }