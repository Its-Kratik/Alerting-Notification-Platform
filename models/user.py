from datetime import datetime
from typing import Dict, Any
from dataclasses import dataclass, asdict

@dataclass
class User:
    id: str
    name: str
    email: str
    team_id: str
    organization_id: str
    is_admin: bool = False
    created_at: datetime = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data['created_at'] = self.created_at.isoformat()
        return data
