import logging
from datetime import datetime
from typing import Dict, Any

class AdminController:
    """Controller for admin operations"""
    
    def __init__(self, db_manager, notification_service):
        self.db_manager = db_manager
        self.notification_service = notification_service
        self.logger = logging.getLogger(__name__)
        
        from services.alert_service import AlertService
        from services.user_service import UserService
        self.alert_service = AlertService(db_manager)
        self.user_service = UserService(db_manager)
    
    def create_alert(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new alert"""
        try:
            # Validate required fields
            required_fields = ['title', 'message', 'severity', 'visibility_type', 'visibility_target', 'start_time', 'expiry_time', 'created_by']
            missing_fields = [field for field in required_fields if field not in request_data]
            
            if missing_fields:
                return self.error_response(f"Missing required fields: {', '.join(missing_fields)}")
            
            # Set defaults
            alert_data = {
                'delivery_type': 'in_app',
                'reminder_frequency_hours': 2,
                'reminders_enabled': True,
                **request_data
            }
            
            alert = self.alert_service.create_alert(alert_data)
            
            # Send initial notification
            users = self.user_service.get_users_for_alert(alert)
            if users:
                delivery_results = self.notification_service.send_alert_to_users(alert, users)
                return self.success_response({
                    'alert': alert.to_dict(),
                    'initial_delivery': delivery_results
                }, "Alert created and sent successfully", 201)
            else:
                return self.success_response(alert.to_dict(), "Alert created but no target users found", 201)
            
        except ValueError as e:
            return self.error_response(str(e))
        except Exception as e:
            self.logger.error(f"Error creating alert: {str(e)}")
            return self.error_response("Internal server error", 500)
    
    def success_response(self, data: Any, message: str = "Success", status_code: int = 200) -> Dict[str, Any]:
        """Create success response"""
        return {
            'status': 'success',
            'message': message,
            'data': data,
            'timestamp': datetime.now().isoformat(),
            'status_code': status_code
        }
    
    def error_response(self, message: str, status_code: int = 400, error_code: str = None) -> Dict[str, Any]:
        """Create error response"""
        return {
            'status': 'error',
            'message': message,
            'error_code': error_code,
            'timestamp': datetime.now().isoformat(),
            'status_code': status_code
        }
