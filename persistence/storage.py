import json
from typing import List
from incident.models import Incident


class IncidentStorage:
    def __init__(self, file_path: str = "history.json"):
        self.file_path = file_path

    def save_incidents(self, incidents: List[Incident]) -> None:
        """Save incidents to JSON file"""
        with open(self.file_path, 'w') as f:
            json.dump([self._incident_to_dict(i)
                      for i in incidents], f, indent=2)

    def load_incidents(self) -> List[Incident]:
        """Load incidents from JSON file"""
        try:
            with open(self.file_path, 'r') as f:
                data = json.load(f)
                return [self._dict_to_incident(d) for d in data]
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def _incident_to_dict(self, incident: Incident) -> dict:
        """Convert Incident to dictionary for JSON serialization"""
        return {
            "id": incident.id,
            "type": incident.type,
            "priority": incident.priority,
            "description": incident.description,
            "created_at": incident.created_at,
            "assigned_to": incident.assigned_to,
            "status": incident.status
        }

    def _dict_to_incident(self, data: dict) -> Incident:
        """Convert dictionary to Incident object"""
        return Incident(
            id=data["id"],
            type=data["type"],
            priority=data["priority"],
            description=data["description"],
            created_at=data["created_at"],
            assigned_to=data["assigned_to"],
            status=data["status"]
        )
