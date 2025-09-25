# Alerting & Notification Platform

A professional-grade alerting and notification system built with Python, featuring clean OOP design, extensibility, and comprehensive functionality.

## 🚀 Features

### Core Functionality
- ✅ **Alert Management**: Create, update, archive alerts with full CRUD operations
- ✅ **Multi-Channel Delivery**: In-app notifications with extensible design for Email/SMS
- ✅ **Smart Targeting**: Organization, team, or user-level visibility
- ✅ **Intelligent Reminders**: Automatic 2-hour reminder cycles until snoozed/expired
- ✅ **User Controls**: Read/unread tracking, daily snooze functionality
- ✅ **Analytics Dashboard**: Comprehensive metrics and engagement tracking

### Technical Excellence
- 🏗️ **Clean Architecture**: Proper separation of concerns (Models, Services, Controllers)
- 🎨 **Design Patterns**: Strategy, Observer, State, and Factory patterns
- 🔧 **RESTful API**: Complete API endpoints for all functionality
- 💾 **Database Persistence**: SQLite with proper schema design
- ⚡ **Concurrent Processing**: Thread-safe notification delivery
- 🔄 **Background Scheduler**: Automatic reminder processing
- 📊 **Comprehensive Analytics**: System and alert-specific metrics

## 📋 Architecture Overview

### Design Patterns Implemented

1. **Strategy Pattern**: Notification channels (In-App, Email, SMS)
2. **Observer Pattern**: Notification event handling
3. **State Pattern**: User alert preferences (Read/Unread/Snoozed)
4. **Factory Pattern**: Channel creation and management
5. **Single Responsibility**: Each class has one clear purpose
6. **Open/Closed**: Easy to add new channels without modifying existing code

### System Components

```
├── Models (Data Layer)
│   ├── Alert, User, Team
│   ├── NotificationDelivery
│   └── UserAlertPreference
├── Services (Business Logic)
│   ├── AlertService
│   ├── NotificationService
│   ├── UserService, TeamService
│   ├── UserAlertPreferenceService
│   └── AnalyticsService
├── Controllers (API Layer)
│   ├── AdminController
│   ├── UserController
│   └── AnalyticsController
├── Channels (Strategy Pattern)
│   ├── InAppChannel
│   ├── EmailChannel
│   └── SMSChannel
└── Infrastructure
    ├── DatabaseManager
    └── ReminderScheduler
```

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8+
- SQLite3

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd alerting-notification-platform
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Initialize the database**
   ```python
   from database.database_manager import DatabaseManager
   db_manager = DatabaseManager()
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

## 📖 API Documentation

### Admin Endpoints

#### Create Alert
```http
POST /api/admin/alerts
Content-Type: application/json

{
    "title": "Critical System Alert",
    "message": "Database server is down",
    "severity": "critical",
    "visibility_type": "organization", 
    "visibility_target": "org_001",
    "start_time": "2025-09-25T18:00:00",
    "expiry_time": "2025-09-26T06:00:00",
    "created_by": "admin_user_id"
}
```

#### Get Admin Alerts
```http
GET /api/admin/alerts?admin_id=admin_user_id&severity=critical&status=active
```

#### Update Alert
```http
PUT /api/admin/alerts/{alert_id}
Content-Type: application/json

{
    "title": "Updated Alert Title",
    "message": "Updated message"
}
```

#### Archive Alert
```http
POST /api/admin/alerts/{alert_id}/archive
```

### User Endpoints

#### Get User Alerts
```http
GET /api/users/{user_id}/alerts
```

#### Mark Alert as Read
```http
POST /api/users/{user_id}/alerts/{alert_id}/read
```

#### Snooze Alert
```http
POST /api/users/{user_id}/alerts/{alert_id}/snooze
```

### Analytics Endpoints

#### System Analytics
```http
GET /api/analytics/system
```

#### Alert Analytics
```http
GET /api/analytics/alerts/{alert_id}
```

## 🎯 Usage Examples

### Creating Alerts Programmatically

```python
from services.alert_service import AlertService
from database.database_manager import DatabaseManager

db_manager = DatabaseManager()
alert_service = AlertService(db_manager)

# Create organization-wide critical alert
alert_data = {
    'title': 'System Maintenance',
    'message': 'Scheduled maintenance tonight 2-4 AM',
    'severity': 'warning',
    'delivery_type': 'in_app',
    'visibility_type': 'organization',
    'visibility_target': 'org_001',
    'start_time': '2025-09-25T18:00:00',
    'expiry_time': '2025-09-26T06:00:00',
    'created_by': 'admin_id'
}

alert = alert_service.create_alert(alert_data)
```

### User Interactions

```python
from services.user_alert_preference_service import UserAlertPreferenceService

preference_service = UserAlertPreferenceService(db_manager)

# Mark alert as read
preference_service.mark_alert_as_read('user_id', 'alert_id')

# Snooze alert for the day
preference_service.snooze_alert('user_id', 'alert_id')
```

### Analytics

```python
from services.analytics_service import AnalyticsService

analytics = AnalyticsService(db_manager)

# Get system-wide metrics
metrics = analytics.get_system_metrics()
print(f"Total alerts: {metrics['overview']['total_alerts_created']}")
print(f"Read rate: {metrics['delivery_metrics']['read_rate']}%")

# Get specific alert analytics
alert_analytics = analytics.get_alert_analytics('alert_id')
```

## 🔧 Configuration

### Notification Channels

The system supports multiple notification channels through the Strategy pattern:

```python
from notification_channels import InAppChannel, EmailChannel, SMSChannel
from services.notification_service import NotificationService

notification_service = NotificationService(db_manager)

# Register additional channels
email_channel = EmailChannel(smtp_config={'server': 'smtp.gmail.com'})
notification_service.register_channel('email', email_channel)
```

### Reminder Frequency

Default reminder frequency is 2 hours, but can be customized:

```python
# In alert creation
alert_data = {
    # ... other fields
    'reminder_frequency_hours': 4,  # Remind every 4 hours
    'reminders_enabled': True
}
```

## 📊 Analytics & Monitoring

### System Metrics
- Total alerts created
- Active vs expired alerts  
- Delivery success rates
- Read/unread rates
- Snooze patterns
- Severity breakdown

### Alert-Specific Analytics
- Delivery statistics
- User engagement rates
- Timeline analysis
- Response patterns

## 🧪 Testing

### Run Demo
```python
python -c "from demo import run_comprehensive_demo; run_comprehensive_demo()"
```

### Unit Tests (Future Enhancement)
```bash
python -m pytest tests/
```

## 🚀 Deployment

### Production Considerations

1. **Database**: Replace SQLite with PostgreSQL/MySQL for production
2. **Message Queue**: Add Redis/RabbitMQ for reliable delivery
3. **Caching**: Implement Redis for frequently accessed data
4. **Monitoring**: Add logging, metrics, and health checks
5. **Security**: Add authentication, authorization, and rate limiting

### Docker Deployment
```dockerfile
FROM python:3.9-slim
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["python", "app.py"]
```

## 🔮 Future Enhancements

- [ ] Email & SMS delivery channels
- [ ] Customizable reminder frequencies
- [ ] Scheduled alerts (cron-like)
- [ ] Alert escalations
- [ ] Role-based access control
- [ ] Push notification integration
- [ ] Advanced analytics dashboard
- [ ] Multi-tenant support

## 📄 License

This project is licensed under the MIT License.

## 👥 Contributing

1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Create Pull Request

## 📞 Support

For support, please contact the development team or create an issue in the repository.