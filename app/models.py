from pydantic import BaseModel
from typing import List, Optional

class Email(BaseModel):
    id: int
    sender: str
    subject: str
    body: str
    thread: List[str]
    is_spam: bool
    is_urgent: bool
    requires_response: bool
    risk_score: float

class Observation(BaseModel):
    current_email: Email
    inbox_remaining: int
    memory_summary: List[str]
    reputation: float
    step_count: int
    goal: str

class Action(BaseModel):
    action_type: str
    email_id: int
    response: Optional[str] = None
