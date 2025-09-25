import sqlite3
import uuid
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any

class AlertService:
    """Service for managing alerts with CRUD operations"""
    
    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.logger = logging.getLogger(__name__)
    
    def create_alert(self, alert_data: Dict[str, Any]):
        """Create a new alert"""
        from models.alert import Alert, Severity, DeliveryType, VisibilityType
        
        alert = Alert(
            id=str(uuid.uuid4()),
            title=alert_data['title'],
            message=alert_data['message'],
            severity=Severity(alert_data['severity']),
            delivery_type=DeliveryType(alert_data['delivery_type']),
            visibility_type=VisibilityType(alert_data['visibility_type']),
            visibility_target=alert_data['visibility_target'],
            start_time=datetime.fromisoformat(alert_data['start_time']),
            expiry_time=datetime.fromisoformat(alert_data['expiry_time']),
            reminder_frequency_hours=alert_data.get('reminder_frequency_hours', 2),
            reminders_enabled=alert_data.get('reminders_enabled', True),
            created_by=alert_data['created_by']
        )
        
        self._save_alert(alert)
        self.logger.info(f"Alert created: {alert.id} - {alert.title}")
        return alert
    
    def update_alert(self, alert_id: str, update_data: Dict[str, Any]):
        """Update an existing alert"""
        alert = self.get_alert_by_id(alert_id)
        if not alert:
            return None
        
        # Update logic here...
        alert.updated_at = datetime.now()
        self._save_alert(alert, is_update=True)
        return alert
    
    def get_alert_by_id(self, alert_id: str):
        """Get alert by ID"""
        conn = sqlite3.connect(self.db_manager.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM alerts WHERE id = ?", (alert_id,))
        row = cursor.fetchone()
        conn.close()
        
        if not row:
            return None
        
        return self._row_to_alert(row)
    
    def get_active_alerts(self):
        """Get all active alerts"""
        conn = sqlite3.connect(self.db_manager.db_path)
        cursor = conn.cursor()
        
        now = datetime.now().isoformat()
        cursor.execute("""
            SELECT * FROM alerts 
            WHERE status = 'active' 
            AND start_time <= ? 
            AND expiry_time >= ?
        """, (now, now))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [self._row_to_alert(row) for row in rows]
    
    def _save_alert(self, alert, is_update: bool = False):
        """Save alert to database"""
        conn = sqlite3.connect(self.db_manager.db_path)
        cursor = conn.cursor()
        
        if is_update:
            # Update SQL here
            pass
        else:
            cursor.execute("""
                INSERT INTO alerts (
                    id, title, message, severity, delivery_type,
                    visibility_type, visibility_target, start_time, expiry_time,
                    reminder_frequency_hours, reminders_enabled, created_by,
                    created_at, updated_at, status
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                alert.id, alert.title, alert.message, alert.severity.value,
                alert.delivery_type.value, alert.visibility_type.value,
                alert.visibility_target, alert.start_time.isoformat(),
                alert.expiry_time.isoformat(), alert.reminder_frequency_hours,
                alert.reminders_enabled, alert.created_by, alert.created_at.isoformat(),
                alert.updated_at.isoformat(), alert.status.value
            ))
        
        conn.commit()
        conn.close()
    
    def _row_to_alert(self, row):
        """Convert database row to Alert object"""
        from models.alert import Alert, Severity, DeliveryType, VisibilityType, AlertStatus
        
        return Alert(
            id=row, title=row, message=row,
            severity=Severity(row), delivery_type=DeliveryType(row),
            visibility_type=VisibilityType(row), visibility_target=row,
            start_time=datetime.fromisoformat(row),
            expiry_time=datetime.fromisoformat(row),
            reminder_frequency_hours=row, reminders_enabled=bool(row),
            created_by=row, created_at=datetime.fromisoformat(row),
            updated_at=datetime.fromisoformat(row),
            status=AlertStatus(row)
        )
