from typing import Deque, Optional, List
from collections import deque
from incident.models import Incident


class IncidentDispatcher:
    def __init__(self):
        self.pending_queue: Deque[Incident] = deque()
        self.in_progress: List[Incident] = []
        self.operators: set[str] = set()
        self.history: List[Incident] = []
        self.all_incidents: List[Incident] = []

    def register_incident(self, incident: Incident) -> None:
        """Register a new incident in the appropriate queue based on priority"""
        if incident.priority == "high":
            self.pending_queue.appendleft(incident)
        else:
            self.pending_queue.append(incident)

    def get_next_incident(self) -> Optional[Incident]:
        """Get the next incident to be handled, respecting priority"""
        return self.pending_queue[0] if self.pending_queue else None

    def assign_incident(self, incident_id: int, operator: str) -> Optional[Incident]:
        """Assign an incident to an operator"""
        incident = self._find_incident_by_id(incident_id)
        if incident and incident.status == "pending":
            self.pending_queue.remove(incident)
            incident = Incident(
                id=incident.id,
                type=incident.type,
                priority=incident.priority,
                description=incident.description,
                created_at=incident.created_at,
                assigned_to=operator,
                status="in_progress"
            )
            self.in_progress.append(incident)
            return incident
        return None

    def resolve_incident(self, incident_id: int) -> Optional[Incident]:
        """Mark an incident as resolved"""
        incident = self._find_incident_in_progress(incident_id)
        if incident:
            self.in_progress.remove(incident)
            resolved = Incident(
                id=incident.id,
                type=incident.type,
                priority=incident.priority,
                description=incident.description,
                created_at=incident.created_at,
                assigned_to=incident.assigned_to,
                status="resolved"
            )
            self.history.append(resolved)
            return resolved
        return None

    def _find_incident_by_id(self, incident_id: int) -> Optional[Incident]:
        """Find an incident by ID in pending queue"""
        for incident in self.pending_queue:
            if incident.id == incident_id:
                return incident
        return None

    def _find_incident_in_progress(self, incident_id: int) -> Optional[Incident]:
        """Find an incident by ID in in_progress list"""
        for incident in self.in_progress:
            if incident.id == incident_id:
                return incident
        return None
