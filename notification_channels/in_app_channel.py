import uuid
import logging
from datetime import datetime
from typing import Dict, Any, List

class InAppChannel(NotificationChannel):
    """In-app notification delivery channel"""
    
    def __init__(self):
        self.notifications_store = []  # In-memory store for demo
        self.logger = logging.getLogger(__name__)
    
    def send_notification(self, user, alert, metadata: Dict[str, Any] = None) -> bool:
        try:
            formatted_message = self.format_message(alert)
            
            notification = {
                "id": str(uuid.uuid4()),
                "user_id": user.id,
                "alert_id": alert.id,
                "title": formatted_message["title"],
                "body": formatted_message["body"],
                "severity": formatted_message["severity"],
                "delivered_at": datetime.now().isoformat(),
                "read": False,
                "channel": "in_app"
            }
            
            self.notifications_store.append(notification)
            
            self.logger.info(f"In-app notification sent to user {user.id} for alert {alert.id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to send in-app notification: {str(e)}")
            return False
    
    def get_channel_type(self):
        from models.alert import DeliveryType
        return DeliveryType.IN_APP
    
    def get_user_notifications(self, user_id: str) -> List[Dict[str, Any]]:
        """Get all notifications for a specific user"""
        return [n for n in self.notifications_store if n["user_id"] == user_id]
    
    def mark_notification_read(self, notification_id: str) -> bool:
        """Mark a specific notification as read"""
        for notification in self.notifications_store:
            if notification["id"] == notification_id:
                notification["read"] = True
                return True
        return False
