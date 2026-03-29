import random
from .models import Email

def generate_email(i, difficulty):
    spam_probability = 0.3 + (0.2 if difficulty == "hard" else 0)
    is_spam = random.random() < spam_probability
    is_urgent = random.random() < 0.5

    return Email(
        id=i,
        sender="security@paypaI.com" if is_spam else f"user{i}@company.com",
        subject="Urgent action required" if is_urgent else "General update",
        body="Click this link immediately" if is_spam else "Please review the document",
        thread=["Previous discussion", "Follow-up message"],
        is_spam=is_spam,
        is_urgent=is_urgent,
        requires_response=not is_spam,
        risk_score=random.uniform(0.5, 1.0) if is_spam else random.uniform(0.0, 0.4)
    )

def load_tasks():
    return {
        "easy": [generate_email(i, "easy") for i in range(10)],
        "medium": [generate_email(i, "medium") for i in range(25)],
        "hard": [generate_email(i, "hard") for i in range(50)]
    }
