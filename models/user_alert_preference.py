from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from enum import Enum
from dataclasses import dataclass, asdict

class UserAlertState(Enum):
    UNREAD = "unread"
    READ = "read"
    SNOOZED = "snoozed"

@dataclass
class UserAlertPreference:
    id: str
    user_id: str
    alert_id: str
    state: UserAlertState
    snoozed_until: Optional[datetime] = None
    last_reminded_at: Optional[datetime] = None
    read_at: Optional[datetime] = None
    created_at: datetime = None
    updated_at: datetime = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.updated_at is None:
            self.updated_at = datetime.now()
    
    def is_snoozed(self) -> bool:
        if self.snoozed_until is None:
            return False
        return datetime.now() < self.snoozed_until
    
    def snooze_for_day(self):
        """Snooze until next day at midnight"""
        tomorrow = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)
        self.snoozed_until = tomorrow
        self.state = UserAlertState.SNOOZED
        self.updated_at = datetime.now()
    
    def mark_as_read(self):
        self.state = UserAlertState.READ
        self.read_at = datetime.now()
        self.updated_at = datetime.now()
    
    def should_remind(self, reminder_frequency_hours: int) -> bool:
        if self.is_snoozed():
            return False
        
        if self.last_reminded_at is None:
            return True
            
        time_since_last_reminder = datetime.now() - self.last_reminded_at
        return time_since_last_reminder >= timedelta(hours=reminder_frequency_hours)
    
    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data['state'] = self.state.value
        data['snoozed_until'] = self.snoozed_until.isoformat() if self.snoozed_until else None
        data['last_reminded_at'] = self.last_reminded_at.isoformat() if self.last_reminded_at else None
        data['read_at'] = self.read_at.isoformat() if self.read_at else None
        data['created_at'] = self.created_at.isoformat()
        data['updated_at'] = self.updated_at.isoformat()
        return data
