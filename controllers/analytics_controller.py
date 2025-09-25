from datetime import datetime
from services.analytics_service import AnalyticsService

class AnalyticsController:
    def __init__(self, db):
        self.metrics = AnalyticsService(db)

    def get_system_analytics(self):
        return {
            "status": "success",
            "data": self.metrics.get_system_metrics(),
            "timestamp": datetime.now().isoformat()
        }

    def get_alert_analytics(self, aid):
        return {"status": "success"}  # stub for brevity
