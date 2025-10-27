from flask import Blueprint, request, jsonify
from auth import AuthService, token_required

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['email', 'password', 'first_name', 'last_name']
        if not all(field in data for field in required_fields):
            return jsonify({'success': False, 'message': 'Missing required fields'}), 400
        
        result = AuthService.register_user(
            email=data['email'],
            password=data['password'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            phone_number=data.get('phone_number')
        )
        
        status_code = 201 if result['success'] else 400
        return jsonify(result), status_code
    
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    """Login user and return JWT token"""
    try:
        data = request.get_json()
        
        if not data.get('email') or not data.get('password'):
            return jsonify({'success': False, 'message': 'Email and password required'}), 400
        
        result = AuthService.login_user(data['email'], data['password'])
        
        status_code = 200 if result['success'] else 401
        return jsonify(result), status_code
    
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500

@auth_bp.route('/verify-token', methods=['GET'])
@token_required
def verify_token(user):
    """Verify if user is logged in"""
    return jsonify({
        'success': True,
        'message': 'User is logged in',
        'user': {
            'id': user['id'],
            'email': user['email'],
            'first_name': user['first_name'],
            'last_name': user['last_name'],
            'verification_status': user['verification_status'],
            'kyc_status': user['kyc_status']
        }
    }), 200

@auth_bp.route('/profile', methods=['GET'])
@token_required
def get_profile(user):
    """Get current user profile"""
    return jsonify({
        'success': True,
        'user': user
    }), 200
