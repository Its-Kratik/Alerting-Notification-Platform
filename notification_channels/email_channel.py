import logging
from models.alert import DeliveryType
from .base_channel import NotificationChannel

class EmailChannel(NotificationChannel):
    def __init__(self, smtp_config=None):
        self.smtp = smtp_config or {}
        self.log = logging.getLogger(__name__)

    def send_notification(self, user, alert, metadata=None):
        self.log.info("EMAIL -> %s : %s", user.email, alert.title)
        return True

    def get_channel_type(self):
        return DeliveryType.EMAIL
