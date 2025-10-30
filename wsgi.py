import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from app import create_app
    app = create_app(os.getenv('FLASK_ENV', 'production'))
    print("[v0] Flask app created successfully")
except Exception as e:
    print(f"[v0] Error creating Flask app: {e}")
    import traceback
    traceback.print_exc()
    # Create a minimal app that shows the error
    from flask import Flask, jsonify
    app = Flask(__name__)
    
    @app.route('/')
    def error():
        return jsonify({
            'success': False,
            'message': f'Failed to initialize app: {str(e)}'
        }), 500

if __name__ == '__main__':
    app.run()
