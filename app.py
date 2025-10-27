from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import config
from database import db
import os

# Import routes
from routes.auth_routes import auth_bp
from routes.items_routes import items_bp
from routes.rentals_routes import rentals_bp
from routes.categories_routes import categories_bp
from routes.users_routes import users_bp

def create_app(config_name='development'):
    """Application factory"""
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    CORS(app, resources={r"/api/*": {"origins": app.config['CORS_ORIGINS']}})
    jwt = JWTManager(app)
    
    # Connect to database
    db.connect()
    
    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(items_bp)
    app.register_blueprint(rentals_bp)
    app.register_blueprint(categories_bp)
    app.register_blueprint(users_bp)
    
    # Health check endpoint
    @app.route('/api/health', methods=['GET'])
    def health_check():
        return jsonify({
            'success': True,
            'message': 'Backend is running',
            'status': 'healthy'
        }), 200
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'message': 'Endpoint not found'
        }), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({
            'success': False,
            'message': 'Internal server error'
        }), 500
    
    # Cleanup on shutdown
    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db.disconnect()
    
    return app

if __name__ == '__main__':
    app = create_app(os.getenv('FLASK_ENV', 'development'))
    app.run(debug=True, host='0.0.0.0', port=5000)
