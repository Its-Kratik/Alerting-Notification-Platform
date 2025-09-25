import sqlite3, uuid
from models.team import Team

class TeamService:
    def __init__(self, db):
        self.db = db

    def create_team(self, data):
        t = Team(id=str(uuid.uuid4()), name=data["name"], organization_id=data["organization_id"])
        self.db.execute("INSERT INTO teams VALUES(?,?,?,?)",
                        (t.id, t.name, t.organization_id, t.created_at.isoformat()))
        return t
