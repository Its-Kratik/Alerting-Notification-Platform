import logging
from models.alert import DeliveryType
from .base_channel import NotificationChannel

class SMSChannel(NotificationChannel):
    def __init__(self, sms_cfg=None):
        self.cfg = sms_cfg or {}
        self.log = logging.getLogger(__name__)

    def send_notification(self, user, alert, metadata=None):
        self.log.info("SMS -> %s : %s", getattr(user, "phone_number", "n/a"), alert.title)
        return True

    def get_channel_type(self):
        return DeliveryType.SMS
