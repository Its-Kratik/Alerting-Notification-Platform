from abc import ABC, abstractmethod
import logging
from typing import Dict, Any

class NotificationChannel(ABC):
    """Abstract base class for notification delivery channels"""
    
    @abstractmethod
    def send_notification(self, user, alert, metadata: Dict[str, Any] = None) -> bool:
        """Send notification to user through this channel"""
        pass
    
    @abstractmethod
    def get_channel_type(self):
        """Return the channel type"""
        pass
    
    def format_message(self, alert) -> Dict[str, str]:
        """Common message formatting logic"""
        severity_icon = {
            Severity.INFO: "ℹ️",
            Severity.WARNING: "⚠️",
            Severity.CRITICAL: "🚨"
        }
        
        return {
            "title": f"{severity_icon.get(alert.severity, '')} {alert.title}",
            "body": alert.message,
            "severity": alert.severity.value,
            "alert_id": alert.id
        }
