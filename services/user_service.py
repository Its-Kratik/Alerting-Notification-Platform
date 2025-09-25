import sqlite3, uuid
from models.user import User

class UserService:
    def __init__(self, db):
        self.db = db

    def create_user(self, data):
        user = User(
            id=str(uuid.uuid4()),
            name=data["name"],
            email=data["email"],
            team_id=data["team_id"],
            organization_id=data["organization_id"],
            is_admin=data.get("is_admin", False)
        )
        self._save(user)
        return user

    def get_user_by_id(self, uid):
        row = self.db.fetchone("SELECT * FROM users WHERE id=?", (uid,))
        return self._row_to_model(row) if row else None

    def get_users_for_team(self, tid):
        return [self._row_to_model(r)
                for r in self.db.fetchall("SELECT * FROM users WHERE team_id=?", (tid,))]

    def _save(self, u):
        self.db.execute(
            "INSERT INTO users VALUES(?,?,?,?,?,?,?)",
            (u.id,u.name,u.email,u.team_id,u.organization_id,u.is_admin,u.created_at.isoformat())
        )

    def _row_to_model(self, r):
        return User(
            id=r[0], name=r[1], email=r[2], team_id=r[3],
            organization_id=r[4], is_admin=bool(r[5])
        )
