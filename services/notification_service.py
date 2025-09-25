import threading
import logging
from typing import Dict, List, Any
from concurrent.futures import ThreadPoolExecutor

class NotificationService:
    """Service for handling notification delivery with Observer pattern"""
    
    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.channels = {}
        self.observers = []  # Observer pattern for notification events
        self.logger = logging.getLogger(__name__)
        
        # Initialize default in-app channel
        from notification_channels.in_app_channel import InAppChannel
        from models.alert import DeliveryType
        self.register_channel(DeliveryType.IN_APP, InAppChannel())
    
    def register_channel(self, channel_type, channel):
        """Register a notification channel"""
        self.channels[channel_type] = channel
        self.logger.info(f"Channel registered: {channel_type.value}")
    
    def send_alert_to_users(self, alert, users: List) -> Dict[str, Any]:
        """Send alert to multiple users"""
        results = {
            'successful_deliveries': 0,
            'failed_deliveries': 0,
            'delivery_details': []
        }
        
        channel = self.channels.get(alert.delivery_type)
        if not channel:
            self.logger.error(f"No channel available for type: {alert.delivery_type}")
            return results
        
        # Use thread pool for concurrent delivery
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = []
            
            for user in users:
                future = executor.submit(self._deliver_to_user, alert, user, channel)
                futures.append((future, user))
            
            # Collect results
            for future, user in futures:
                try:
                    success = future.result(timeout=30)  # 30 second timeout
                    
                    if success:
                        results['successful_deliveries'] += 1
                    else:
                        results['failed_deliveries'] += 1
                    
                    results['delivery_details'].append({
                        'user_id': user.id,
                        'user_name': user.name,
                        'success': success
                    })
                    
                except Exception as e:
                    self.logger.error(f"Delivery failed for user {user.id}: {str(e)}")
                    results['failed_deliveries'] += 1
        
        return results
    
    def _deliver_to_user(self, alert, user, channel) -> bool:
        """Deliver notification to a single user"""
        try:
            # Send notification
            success = channel.send_notification(user, alert)
            
            if success:
                # Log delivery
                self._log_delivery(alert, user, channel.get_channel_type())
            
            return success
            
        except Exception as e:
            self.logger.error(f"Failed to deliver to user {user.id}: {str(e)}")
            return False
    
    def _log_delivery(self, alert, user, channel_type):
        """Log notification delivery"""
        from models.notification_delivery import NotificationDelivery
        from datetime import datetime
        
        delivery = NotificationDelivery(
            id=str(uuid.uuid4()),
            alert_id=alert.id,
            user_id=user.id,
            delivery_channel=channel_type,
            delivered_at=datetime.now()
        )
        
        conn = sqlite3.connect(self.db_manager.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO notification_deliveries 
            (id, alert_id, user_id, delivery_channel, delivered_at, delivery_status)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            delivery.id, delivery.alert_id, delivery.user_id,
            delivery.delivery_channel.value, delivery.delivered_at.isoformat(),
            delivery.delivery_status
        ))
        
        conn.commit()
        conn.close()
