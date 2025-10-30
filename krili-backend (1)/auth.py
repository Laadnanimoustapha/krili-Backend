import bcrypt
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from database import db

class AuthService:
    """Authentication service"""
    
    @staticmethod
    def hash_password(password):
        """Hash password using bcrypt"""
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    
    @staticmethod
    def verify_password(password, password_hash):
        """Verify password against hash"""
        return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))
    
    @staticmethod
    def register_user(email, password, first_name, last_name, phone_number=None):
        """Register a new user"""
        try:
            # Check if user already exists
            existing_user = db.execute_query_single(
                "SELECT id FROM users WHERE email = %s",
                (email,)
            )
            
            if existing_user:
                return {'success': False, 'message': 'Email already registered'}
            
            # Hash password
            password_hash = AuthService.hash_password(password)
            
            # Insert new user
            query = """
                INSERT INTO users (email, password_hash, first_name, last_name, phone_number)
                VALUES (%s, %s, %s, %s, %s)
            """
            result = db.execute_query(query, (email, password_hash, first_name, last_name, phone_number))
            
            if result:
                return {'success': True, 'message': 'User registered successfully'}
            else:
                return {'success': False, 'message': 'Registration failed'}
        
        except Exception as e:
            return {'success': False, 'message': f'Error: {str(e)}'}
    
    @staticmethod
    def login_user(email, password):
        """Authenticate user and return JWT token"""
        try:
            # Get user from database
            user = db.execute_query_single(
                "SELECT id, email, password_hash, first_name, last_name FROM users WHERE email = %s",
                (email,)
            )
            
            if not user:
                return {'success': False, 'message': 'Invalid email or password'}
            
            # Verify password
            if not AuthService.verify_password(password, user['password_hash']):
                return {'success': False, 'message': 'Invalid email or password'}
            
            # Update last login
            db.execute_query(
                "UPDATE users SET last_login_at = NOW() WHERE id = %s",
                (user['id'],)
            )
            
            # Create JWT token
            access_token = create_access_token(
                identity=user['id'],
                expires_delta=timedelta(days=1)
            )
            
            return {
                'success': True,
                'message': 'Login successful',
                'token': access_token,
                'user': {
                    'id': user['id'],
                    'email': user['email'],
                    'first_name': user['first_name'],
                    'last_name': user['last_name']
                }
            }
        
        except Exception as e:
            return {'success': False, 'message': f'Error: {str(e)}'}
    
    @staticmethod
    def get_user_by_id(user_id):
        """Get user information by ID"""
        try:
            user = db.execute_query_single(
                """
                SELECT id, email, first_name, last_name, phone_number, profile_picture_url, 
                       bio, location, city, country, verification_status, kyc_status, 
                       rating, total_reviews, total_rentals_as_renter, total_rentals_as_owner
                FROM users WHERE id = %s AND is_active = TRUE
                """,
                (user_id,)
            )
            return user
        except Exception as e:
            print(f"Error getting user: {str(e)}")
            return None

def token_required(f):
    """Decorator to check JWT token"""
    @wraps(f)
    @jwt_required()
    def decorated(*args, **kwargs):
        user_id = get_jwt_identity()
        user = AuthService.get_user_by_id(user_id)
        
        if not user:
            return jsonify({'success': False, 'message': 'User not found'}), 401
        
        return f(user, *args, **kwargs)
    
    return decorated

def optional_token(f):
    """Decorator for optional JWT token"""
    @wraps(f)
    def decorated(*args, **kwargs):
        user = None
        try:
            from flask_jwt_extended import verify_jwt_in_request
            verify_jwt_in_request(optional=True)
            user_id = get_jwt_identity()
            if user_id:
                user = AuthService.get_user_by_id(user_id)
        except:
            pass
        
        return f(user, *args, **kwargs)
    
    return decorated
