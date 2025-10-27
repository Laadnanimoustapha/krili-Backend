from flask import Blueprint, request, jsonify
from auth import token_required
from database import db
from datetime import datetime

rentals_bp = Blueprint('rentals', __name__, url_prefix='/api/rentals')

@rentals_bp.route('', methods=['POST'])
@token_required
def create_rental(user):
    """Create a new rental booking"""
    try:
        data = request.get_json()
        
        required_fields = ['item_id', 'rental_start_date', 'rental_end_date']
        if not all(field in data for field in required_fields):
            return jsonify({'success': False, 'message': 'Missing required fields'}), 400
        
        # Get item details
        item = db.execute_query_single(
            "SELECT * FROM items WHERE id = %s AND listing_status = 'active'",
            (data['item_id'],)
        )
        
        if not item:
            return jsonify({'success': False, 'message': 'Item not found'}), 404
        
        if item['owner_id'] == user['id']:
            return jsonify({'success': False, 'message': 'Cannot rent your own item'}), 400
        
        # Calculate rental duration
        start_date = datetime.strptime(data['rental_start_date'], '%Y-%m-%d')
        end_date = datetime.strptime(data['rental_end_date'], '%Y-%m-%d')
        duration_days = (end_date - start_date).days
        
        if duration_days <= 0:
            return jsonify({'success': False, 'message': 'Invalid rental dates'}), 400
        
        # Calculate prices
        daily_price = float(item['daily_rental_price'])
        subtotal = daily_price * duration_days
        security_deposit = float(item['security_deposit']) if item['security_deposit'] else 0
        insurance_price = float(data.get('insurance_price', 0))
        delivery_price = float(data.get('delivery_price', 0))
        total_price = subtotal + security_deposit + insurance_price + delivery_price
        
        # Create rental
        query = """
            INSERT INTO rentals (item_id, renter_id, owner_id, rental_start_date, rental_end_date,
                               rental_duration_days, daily_price, subtotal, security_deposit,
                               insurance_price, delivery_price, total_price, pickup_location,
                               delivery_location, notes)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        params = (
            data['item_id'],
            user['id'],
            item['owner_id'],
            data['rental_start_date'],
            data['rental_end_date'],
            duration_days,
            daily_price,
            subtotal,
            security_deposit,
            insurance_price,
            delivery_price,
            total_price,
            data.get('pickup_location'),
            data.get('delivery_location'),
            data.get('notes')
        )
        
        result = db.execute_query(query, params)
        
        if result:
            return jsonify({
                'success': True,
                'message': 'Rental created successfully',
                'rental_id': result,
                'total_price': total_price
            }), 201
        else:
            return jsonify({'success': False, 'message': 'Failed to create rental'}), 400
    
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500

@rentals_bp.route('/user', methods=['GET'])
@token_required
def get_user_rentals(user):
    """Get rentals for current user (as renter and owner)"""
    try:
        rental_type = request.args.get('type', 'all')  # 'renter', 'owner', 'all'
        status = request.args.get('status')
        
        if rental_type in ['renter', 'all']:
            renter_query = """
                SELECT r.*, i.title as item_title, i.daily_rental_price,
                       u.first_name, u.last_name, u.profile_picture_url
                FROM rentals r
                JOIN items i ON r.item_id = i.id
                JOIN users u ON r.owner_id = u.id
                WHERE r.renter_id = %s
            """
            params = [user['id']]
            
            if status:
                renter_query += " AND r.rental_status = %s"
                params.append(status)
            
            renter_query += " ORDER BY r.created_at DESC"
            renter_rentals = db.execute_query(renter_query, params)
        else:
            renter_rentals = []
        
        if rental_type in ['owner', 'all']:
            owner_query = """
                SELECT r.*, i.title as item_title, i.daily_rental_price,
                       u.first_name, u.last_name, u.profile_picture_url
                FROM rentals r
                JOIN items i ON r.item_id = i.id
                JOIN users u ON r.renter_id = u.id
                WHERE r.owner_id = %s
            """
            params = [user['id']]
            
            if status:
                owner_query += " AND r.rental_status = %s"
                params.append(status)
            
            owner_query += " ORDER BY r.created_at DESC"
            owner_rentals = db.execute_query(owner_query, params)
        else:
            owner_rentals = []
        
        return jsonify({
            'success': True,
            'renter_rentals': renter_rentals,
            'owner_rentals': owner_rentals
        }), 200
    
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500
