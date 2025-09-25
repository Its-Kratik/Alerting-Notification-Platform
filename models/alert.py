from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from enum import Enum
from dataclasses import dataclass, asdict

class Severity(Enum):
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"

class DeliveryType(Enum):
    IN_APP = "in_app"
    EMAIL = "email"
    SMS = "sms"

class VisibilityType(Enum):
    ORGANIZATION = "organization"
    TEAM = "team"
    USER = "user"

class AlertStatus(Enum):
    ACTIVE = "active"
    EXPIRED = "expired"
    ARCHIVED = "archived"

@dataclass
class Alert:
    id: str
    title: str
    message: str
    severity: Severity
    delivery_type: DeliveryType
    visibility_type: VisibilityType
    visibility_target: str  # org_id, team_id, or user_id
    start_time: datetime
    expiry_time: datetime
    reminder_frequency_hours: int = 2
    reminders_enabled: bool = True
    created_by: str = ""
    created_at: datetime = None
    updated_at: datetime = None
    status: AlertStatus = AlertStatus.ACTIVE
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.updated_at is None:
            self.updated_at = datetime.now()
    
    def is_active(self) -> bool:
        now = datetime.now()
        return (self.status == AlertStatus.ACTIVE and 
                self.start_time <= now <= self.expiry_time)
    
    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data['severity'] = self.severity.value
        data['delivery_type'] = self.delivery_type.value
        data['visibility_type'] = self.visibility_type.value
        data['status'] = self.status.value
        data['start_time'] = self.start_time.isoformat()
        data['expiry_time'] = self.expiry_time.isoformat()
        data['created_at'] = self.created_at.isoformat()
        data['updated_at'] = self.updated_at.isoformat()
        return data
