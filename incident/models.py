from dataclasses import dataclass


@dataclass(frozen=True)
class Incident:
    id: int
    type: str  # e.g., "infrastructure", "security", "application"
    priority: str  # "high", "medium", "low"
    description: str
    created_at: str
    assigned_to: str
    status: str  # "pending", "in_progress", "resolved", "escalated"
