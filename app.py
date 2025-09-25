from flask import Flask, request, jsonify
import logging
from database.database_manager import DatabaseManager
from services.notification_service import NotificationService
from controllers.admin_controller import AdminController
from controllers.user_controller import UserController
from controllers.analytics_controller import AnalyticsController

def create_app():
    """Create and configure Flask application"""
    app = Flask(__name__)
    app.config['JSON_SORT_KEYS'] = False
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Initialize services
    db_manager = DatabaseManager()
    notification_service = NotificationService(db_manager)
    
    # Initialize controllers
    admin_controller = AdminController(db_manager, notification_service)
    user_controller = UserController(db_manager)
    analytics_controller = AnalyticsController(db_manager)
    
    # Admin Routes
    @app.route('/api/admin/alerts', methods=['POST'])
    def create_alert():
        return jsonify(admin_controller.create_alert(request.get_json()))
    
    @app.route('/api/admin/alerts/<alert_id>', methods=['PUT'])
    def update_alert(alert_id):
        return jsonify(admin_controller.update_alert(alert_id, request.get_json()))
    
    @app.route('/api/admin/alerts', methods=['GET'])
    def get_admin_alerts():
        admin_id = request.args.get('admin_id', required=True)
        filters = {
            'severity': request.args.get('severity'),
            'status': request.args.get('status'),
            'visibility_type': request.args.get('visibility_type')
        }
        filters = {k: v for k, v in filters.items() if v}
        return jsonify(admin_controller.get_alerts(admin_id, filters))
    
    # User Routes
    @app.route('/api/users/<user_id>/alerts', methods=['GET'])
    def get_user_alerts(user_id):
        return jsonify(user_controller.get_user_alerts(user_id))
    
    @app.route('/api/users/<user_id>/alerts/<alert_id>/read', methods=['POST'])
    def mark_alert_read(user_id, alert_id):
        return jsonify(user_controller.mark_alert_read(user_id, alert_id))
    
    @app.route('/api/users/<user_id>/alerts/<alert_id>/snooze', methods=['POST'])
    def snooze_alert(user_id, alert_id):
        return jsonify(user_controller.snooze_alert(user_id, alert_id))
    
    # Analytics Routes
    @app.route('/api/analytics/system', methods=['GET'])
    def get_system_analytics():
        return jsonify(analytics_controller.get_system_analytics())
    
    @app.route('/api/analytics/alerts/<alert_id>', methods=['GET'])
    def get_alert_analytics(alert_id):
        return jsonify(analytics_controller.get_alert_analytics(alert_id))
    
    # Health check
    @app.route('/api/health', methods=['GET'])
    def health_check():
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'services': {
                'database': 'active',
                'notification_service': 'active'
            }
        })
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
