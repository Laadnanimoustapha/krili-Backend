from flask import Blueprint, request, jsonify
from auth import token_required
from database import db

users_bp = Blueprint('users', __name__, url_prefix='/api/users')

@users_bp.route('/<int:user_id>', methods=['GET'])
def get_user_profile(user_id):
    """Get public user profile"""
    try:
        user = db.execute_query_single(
            """
            SELECT id, first_name, last_name, profile_picture_url, bio, location, city, country,
                   verification_status, rating, total_reviews, total_rentals_as_renter, 
                   total_rentals_as_owner, created_at
            FROM users
            WHERE id = %s AND is_active = TRUE
            """,
            (user_id,)
        )
        
        if not user:
            return jsonify({'success': False, 'message': 'User not found'}), 404
        
        # Get user reviews
        reviews = db.execute_query(
            """
            SELECT r.*, reviewer.first_name, reviewer.last_name, reviewer.profile_picture_url
            FROM reviews r
            JOIN users reviewer ON r.reviewer_id = reviewer.id
            WHERE r.reviewee_id = %s AND r.review_type = 'user'
            ORDER BY r.created_at DESC LIMIT 10
            """,
            (user_id,)
        )
        
        user['reviews'] = reviews
        
        return jsonify({
            'success': True,
            'user': user
        }), 200
    
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500

@users_bp.route('/profile', methods=['PUT'])
@token_required
def update_profile(user):
    """Update current user profile"""
    try:
        data = request.get_json()
        
        # Build update query dynamically
        allowed_fields = ['first_name', 'last_name', 'phone_number', 'bio', 'location', 'city', 'country']
        update_fields = []
        params = []
        
        for field in allowed_fields:
            if field in data:
                update_fields.append(f"{field} = %s")
                params.append(data[field])
        
        if not update_fields:
            return jsonify({'success': False, 'message': 'No fields to update'}), 400
        
        params.append(user['id'])
        
        query = f"UPDATE users SET {', '.join(update_fields)} WHERE id = %s"
        result = db.execute_query(query, params)
        
        if result:
            return jsonify({
                'success': True,
                'message': 'Profile updated successfully'
            }), 200
        else:
            return jsonify({'success': False, 'message': 'Failed to update profile'}), 400
    
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500
