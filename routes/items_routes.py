from flask import Blueprint, request, jsonify
from auth import token_required, optional_token
from database import db

items_bp = Blueprint('items', __name__, url_prefix='/api/items')

@items_bp.route('', methods=['GET'])
@optional_token
def get_items(user):
    """Get all active items with optional filters"""
    try:
        # Get query parameters
        category_id = request.args.get('category_id')
        city = request.args.get('city')
        min_price = request.args.get('min_price')
        max_price = request.args.get('max_price')
        search = request.args.get('search')
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 20))
        offset = (page - 1) * limit
        
        # Build query
        query = """
            SELECT i.*, u.first_name, u.last_name, u.rating, u.profile_picture_url,
                   c.name as category_name, c.slug as category_slug,
                   (SELECT GROUP_CONCAT(image_url) FROM item_images WHERE item_id = i.id AND is_primary = TRUE) as primary_image
            FROM items i
            JOIN users u ON i.owner_id = u.id
            JOIN categories c ON i.category_id = c.id
            WHERE i.listing_status = 'active' AND u.is_active = TRUE
        """
        
        params = []
        
        if category_id:
            query += " AND i.category_id = %s"
            params.append(category_id)
        
        if city:
            query += " AND i.city = %s"
            params.append(city)
        
        if min_price:
            query += " AND i.daily_rental_price >= %s"
            params.append(float(min_price))
        
        if max_price:
            query += " AND i.daily_rental_price <= %s"
            params.append(float(max_price))
        
        if search:
            query += " AND (i.title LIKE %s OR i.description LIKE %s)"
            search_term = f"%{search}%"
            params.extend([search_term, search_term])
        
        query += " ORDER BY i.created_at DESC LIMIT %s OFFSET %s"
        params.extend([limit, offset])
        
        items = db.execute_query(query, params)
        
        # Get total count
        count_query = """
            SELECT COUNT(*) as total FROM items i
            JOIN users u ON i.owner_id = u.id
            WHERE i.listing_status = 'active' AND u.is_active = TRUE
        """
        count_params = []
        
        if category_id:
            count_query += " AND i.category_id = %s"
            count_params.append(category_id)
        if city:
            count_query += " AND i.city = %s"
            count_params.append(city)
        if min_price:
            count_query += " AND i.daily_rental_price >= %s"
            count_params.append(float(min_price))
        if max_price:
            count_query += " AND i.daily_rental_price <= %s"
            count_params.append(float(max_price))
        if search:
            count_query += " AND (i.title LIKE %s OR i.description LIKE %s)"
            search_term = f"%{search}%"
            count_params.extend([search_term, search_term])
        
        total_result = db.execute_query_single(count_query, count_params)
        total = total_result['total'] if total_result else 0
        
        return jsonify({
            'success': True,
            'items': items,
            'pagination': {
                'page': page,
                'limit': limit,
                'total': total,
                'pages': (total + limit - 1) // limit
            }
        }), 200
    
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500

@items_bp.route('/<int:item_id>', methods=['GET'])
@optional_token
def get_item(user, item_id):
    """Get single item details"""
    try:
        item = db.execute_query_single(
            """
            SELECT i.*, u.id as owner_id, u.first_name, u.last_name, u.rating, 
                   u.profile_picture_url, u.bio, u.location, u.total_reviews,
                   c.name as category_name, c.slug as category_slug
            FROM items i
            JOIN users u ON i.owner_id = u.id
            JOIN categories c ON i.category_id = c.id
            WHERE i.id = %s AND i.listing_status = 'active'
            """,
            (item_id,)
        )
        
        if not item:
            return jsonify({'success': False, 'message': 'Item not found'}), 404
        
        # Get item images
        images = db.execute_query(
            "SELECT id, image_url, is_primary FROM item_images WHERE item_id = %s ORDER BY display_order",
            (item_id,)
        )
        
        # Get reviews
        reviews = db.execute_query(
            """
            SELECT r.*, u.first_name, u.last_name, u.profile_picture_url
            FROM reviews r
            JOIN users u ON r.reviewer_id = u.id
            WHERE r.item_id = %s AND r.review_type = 'item'
            ORDER BY r.created_at DESC LIMIT 10
            """,
            (item_id,)
        )
        
        item['images'] = images
        item['reviews'] = reviews
        
        return jsonify({
            'success': True,
            'item': item
        }), 200
    
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500

@items_bp.route('', methods=['POST'])
@token_required
def create_item(user):
    """Create a new item listing"""
    try:
        data = request.get_json()
        
        required_fields = ['title', 'category_id', 'daily_rental_price', 'description']
        if not all(field in data for field in required_fields):
            return jsonify({'success': False, 'message': 'Missing required fields'}), 400
        
        query = """
            INSERT INTO items (owner_id, category_id, title, description, daily_rental_price,
                             weekly_rental_price, monthly_rental_price, security_deposit,
                             location, city, country, condition, quantity_available)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        params = (
            user['id'],
            data['category_id'],
            data['title'],
            data['description'],
            data['daily_rental_price'],
            data.get('weekly_rental_price'),
            data.get('monthly_rental_price'),
            data.get('security_deposit'),
            data.get('location'),
            data.get('city'),
            data.get('country'),
            data.get('condition', 'good'),
            data.get('quantity_available', 1)
        )
        
        result = db.execute_query(query, params)
        
        if result:
            return jsonify({
                'success': True,
                'message': 'Item created successfully',
                'item_id': result
            }), 201
        else:
            return jsonify({'success': False, 'message': 'Failed to create item'}), 400
    
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500
