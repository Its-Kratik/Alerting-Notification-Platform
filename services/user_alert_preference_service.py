import uuid, sqlite3
from datetime import datetime
from models.user_alert_preference import UserAlertPreference, UserAlertState

class UserAlertPreferenceService:
    def __init__(self, db):
        self.db = db

    def get_or_create(self, uid, aid):
        row = self.db.fetchone(
            "SELECT * FROM user_alert_preferences WHERE user_id=? AND alert_id=?", (uid, aid))
        if row:
            return self._row_to_model(row)
        pref = UserAlertPreference(id=str(uuid.uuid4()), user_id=uid, alert_id=aid,
                                   state=UserAlertState.UNREAD)
        self._save(pref)
        return pref

    def mark_read(self, uid, aid):
        p = self.get_or_create(uid, aid)
        p.mark_as_read()
        self._save(p, update=True)
        return True

    def snooze(self, uid, aid):
        p = self.get_or_create(uid, aid)
        p.snooze_for_day()
        self._save(p, update=True)
        return True

    def _save(self, p, update=False):
        if update:
            self.db.execute("""UPDATE user_alert_preferences
                               SET state=?, snoozed_until=?, read_at=?, updated_at=?
                               WHERE id=?""",
                            (p.state.value,
                             p.snoozed_until.isoformat() if p.snoozed_until else None,
                             p.read_at.isoformat() if p.read_at else None,
                             p.updated_at.isoformat(), p.id))
        else:
            self.db.execute("""INSERT INTO user_alert_preferences
                               VALUES(?,?,?,?,?,?,?,?,?)""",
                            (p.id, p.user_id, p.alert_id, p.state.value, None, None,
                             None, p.created_at.isoformat(), p.updated_at.isoformat()))

    def _row_to_model(self, r):
        from datetime import datetime as dt
        return UserAlertPreference(
            id=r[0], user_id=r[1], alert_id=r[2],
            state=UserAlertState(r[3]),
            snoozed_until=dt.fromisoformat(r[4]) if r[4] else None,
            last_reminded_at=dt.fromisoformat(r[5]) if r[5] else None,
            read_at=dt.fromisoformat(r[6]) if r[6] else None,
            created_at=dt.fromisoformat(r[7]),
            updated_at=dt.fromisoformat(r[8])
        )
