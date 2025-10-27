from flask import Blueprint, jsonify
from database import db

categories_bp = Blueprint('categories', __name__, url_prefix='/api/categories')

@categories_bp.route('', methods=['GET'])
def get_categories():
    """Get all active categories"""
    try:
        categories = db.execute_query(
            """
            SELECT id, name, slug, description, icon_url, image_url, display_order
            FROM categories
            WHERE is_active = TRUE
            ORDER BY display_order ASC
            """
        )
        
        return jsonify({
            'success': True,
            'categories': categories
        }), 200
    
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500

@categories_bp.route('/<int:category_id>', methods=['GET'])
def get_category(category_id):
    """Get single category"""
    try:
        category = db.execute_query_single(
            """
            SELECT id, name, slug, description, icon_url, image_url
            FROM categories
            WHERE id = %s AND is_active = TRUE
            """,
            (category_id,)
        )
        
        if not category:
            return jsonify({'success': False, 'message': 'Category not found'}), 404
        
        return jsonify({
            'success': True,
            'category': category
        }), 200
    
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500
