import sqlite3
import logging

class DatabaseManager:
    """Handles database operations with SQLite"""
    
    def __init__(self, db_path: str = "alerting_platform.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize database with required tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                team_id TEXT NOT NULL,
                organization_id TEXT NOT NULL,
                is_admin BOOLEAN DEFAULT FALSE,
                created_at TEXT NOT NULL
            )
        ''')
        
        # Teams table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS teams (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                organization_id TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        ''')
        
        # Alerts table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS alerts (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                message TEXT NOT NULL,
                severity TEXT NOT NULL,
                delivery_type TEXT NOT NULL,
                visibility_type TEXT NOT NULL,
                visibility_target TEXT NOT NULL,
                start_time TEXT NOT NULL,
                expiry_time TEXT NOT NULL,
                reminder_frequency_hours INTEGER DEFAULT 2,
                reminders_enabled BOOLEAN DEFAULT TRUE,
                created_by TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                status TEXT DEFAULT 'active'
            )
        ''')
        
        # Notification deliveries table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS notification_deliveries (
                id TEXT PRIMARY KEY,
                alert_id TEXT NOT NULL,
                user_id TEXT NOT NULL,
                delivery_channel TEXT NOT NULL,
                delivered_at TEXT NOT NULL,
                delivery_status TEXT DEFAULT 'sent',
                FOREIGN KEY (alert_id) REFERENCES alerts (id),
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # User alert preferences table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_alert_preferences (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                alert_id TEXT NOT NULL,
                state TEXT NOT NULL,
                snoozed_until TEXT,
                last_reminded_at TEXT,
                read_at TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (id),
                FOREIGN KEY (alert_id) REFERENCES alerts (id),
                UNIQUE(user_id, alert_id)
            )
        ''')
        
        conn.commit()
        conn.close()
