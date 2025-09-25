from datetime import datetime
from services.user_service import UserService
from services.alert_service import AlertService
from services.user_alert_preference_service import UserAlertPreferenceService

class UserController:
    def __init__(self, db):
        self.user_srv = UserService(db)
        self.alert_srv = AlertService(db)
        self.pref_srv = UserAlertPreferenceService(db)

    def get_user_alerts(self, uid):
        active = self.alert_srv.get_active_alerts()
        result = []
        for a in active:
            users = self.user_srv.get_users_for_team(a.visibility_target) \
                    if a.visibility_type.value == "team" else []
            if any(u.id == uid for u in users):
                pref = self.pref_srv.get_or_create(uid, a.id)
                data = a.to_dict()
                data["state"] = pref.state.value
                result.append(data)
        return {"status": "success", "data": result, "timestamp": datetime.now().isoformat()}

    def mark_alert_read(self, uid, aid):
        self.pref_srv.mark_read(uid, aid)
        return {"status": "success"}

    def snooze_alert(self, uid, aid):
        self.pref_srv.snooze(uid, aid)
        return {"status": "success"}
