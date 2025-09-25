from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum

class Channel(Enum):
    IN_APP = "in_app"
    EMAIL = "email"
    SMS = "sms"

@dataclass
class NotificationDelivery:
    id: str
    alert_id: str
    user_id: str
    delivery_channel: Channel
    delivered_at: datetime = datetime.now()
    delivery_status: str = "sent"

    def to_dict(self):
        d = asdict(self)
        d["delivery_channel"] = self.delivery_channel.value
        d["delivered_at"] = self.delivered_at.isoformat()
        return d
