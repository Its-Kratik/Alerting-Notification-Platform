class AnalyticsService:
    def __init__(self, db):
        self.db = db

    def get_system_metrics(self):
        total_alerts = self.db.scalar("SELECT COUNT(*) FROM alerts")
        total_deliveries = self.db.scalar("SELECT COUNT(*) FROM notification_deliveries")
        reads = self.db.scalar("SELECT COUNT(*) FROM user_alert_preferences WHERE state='read'")
        return {
            "total_alerts": total_alerts,
            "total_deliveries": total_deliveries,
            "read_rate": round((reads/total_deliveries*100) if total_deliveries else 0, 2)
        }
