from typing import Dict, Literal
from dataclasses import dataclass


IncidentTypes = Literal["infrastructure", "security", "application"]


@dataclass(frozen=True)
class IncidentRule:
    allowed_roles: Literal['admin', 'sysadmin', 'network_engineer',
                           'security_analyst', 'security_engineer', 'developer', 'qa_engineer']
    escalation_time_minutes: int


incident_rules: Dict[IncidentTypes, IncidentRule] = {
    "infrastructure": IncidentRule(
        allowed_roles={"admin", "sysadmin", "network_engineer"},
        escalation_time_minutes=30
    ),
    "security": IncidentRule(
        allowed_roles={"admin", "security_analyst", "security_engineer"},
        escalation_time_minutes=15
    ),
    "application": IncidentRule(
        allowed_roles={"admin", "developer", "qa_engineer"},
        escalation_time_minutes=60
    ),
}
