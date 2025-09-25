import threading, time, logging

class ReminderScheduler(threading.Thread):
    def __init__(self, db, notifier, pref_srv):
        super().__init__(daemon=True)
        self.db, self.notify, self.pref = db, notifier, pref_srv
        self.running = False
        self.log = logging.getLogger(__name__)

    def run(self):
        self.running = True
        while self.running:
            alerts = self.pref.get_alerts_needing_reminder()
            for a, users in alerts:
                self.notify.send_alert_to_users(a, users)
            time.sleep(300)
