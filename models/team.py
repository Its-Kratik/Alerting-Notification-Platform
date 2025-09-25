from dataclasses import dataclass, asdict
from datetime import datetime

@dataclass
class Team:
    id: str
    name: str
    organization_id: str
    created_at: datetime = datetime.now()

    def to_dict(self):
        d = asdict(self)
        d["created_at"] = self.created_at.isoformat()
        return d
