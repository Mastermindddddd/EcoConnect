from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
import os
import uuid
from datetime import datetime
from src.models.user import db
from src.models.waste_item import WasteItem
from src.models.recycling_center import RecyclingCenter
from src.services.mock_ai_classifier import MockAIWasteClassifier, save_uploaded_image
import math
import json

waste_identification_bp = Blueprint('waste_identification', __name__)

# Initialize AI classifier
ai_classifier = MockAIWasteClassifier()

# Allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def calculate_distance(lat1, lon1, lat2, lon2):
    """Calculate distance between two points using Haversine formula."""
    R = 6371  # Earth's radius in kilometers
    
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)
    
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    
    a = math.sin(dlat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    
    return R * c

@waste_identification_bp.route('/identify-waste', methods=['POST'])
def identify_waste():
    """
    Identify waste from uploaded image using AI.
    
    Form data:
    - image: Image file
    - user_id: ID of the user (optional)
    - latitude: User's latitude (optional)
    - longitude: User's longitude (optional)
    """
    try:
        # Check if image file is present
        if 'image' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No image file provided'
            }), 400
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({
                'success': False,
                'error': 'No file selected'
            }), 400
        
        if not allowed_file(file.filename):
            return jsonify({
                'success': False,
                'error': 'Invalid file type. Supported formats: PNG, JPG, JPEG, GIF, WebP'
            }), 400
        
        # Get optional parameters
        user_id = request.form.get('user_id', type=int)
        user_latitude = request.form.get('latitude', type=float)
        user_longitude = request.form.get('longitude', type=float)
        
        # Save uploaded image
        upload_dir = os.path.join(os.path.dirname(__file__), '..', 'static', 'uploads')
        image_path = save_uploaded_image(file, upload_dir)
        
        # Classify the waste using AI
        classification_result = ai_classifier.classify_waste(image_path)
        
        # Find recommended recycling center if location provided
        recommended_center = None
        if user_latitude and user_longitude and classification_result.get('recyclable'):
            material_category = classification_result.get('material_category')
            centers = RecyclingCenter.query.filter_by(is_active=True).all()
            
            # Find centers that accept this material type
            suitable_centers = []
            for center in centers:
                if center.accepted_materials:
                    try:
                        # Handle both JSON string and list formats
                        if isinstance(center.accepted_materials, str):
                            accepted_materials = json.loads(center.accepted_materials)
                        else:
                            accepted_materials = center.accepted_materials
                        
                        if material_category in accepted_materials:
                            distance = calculate_distance(
                                user_latitude, user_longitude,
                                center.latitude, center.longitude
                            )
                            suitable_centers.append((center, distance))
                    except (json.JSONDecodeError, TypeError):
                        continue
            
            # Sort by distance and get the closest one
            if suitable_centers:
                suitable_centers.sort(key=lambda x: x[1])
                closest_center, distance = suitable_centers[0]
                recommended_center = {
                    'id': closest_center.id,
                    'name': closest_center.name,
                    'address': closest_center.address,
                    'distance': round(distance, 1),
                    'phone': closest_center.phone,
                    'operating_hours': closest_center.operating_hours
                }
        
        # Save to database if user_id provided
        waste_item_id = None
        if user_id:
            try:
                # Create relative path for database storage
                relative_path = os.path.relpath(image_path, os.path.join(os.path.dirname(__file__), '..', 'static'))
                
                waste_item = WasteItem(
                    user_id=user_id,
                    image_path=f'/static/{relative_path}',
                    identified_type=classification_result.get('identified_type'),
                    confidence_score=classification_result.get('confidence_score', 0.0),
                    material_category=classification_result.get('material_category'),
                    recyclable=classification_result.get('recyclable', False),
                    disposal_method=classification_result.get('disposal_method'),
                    recommended_center_id=recommended_center['id'] if recommended_center else None
                )
                
                db.session.add(waste_item)
                db.session.commit()
                waste_item_id = waste_item.id
                
            except Exception as e:
                print(f"Error saving waste item: {e}")
                db.session.rollback()
                # Continue without saving to database
        
        # Get enhanced recommendations
        user_location = None
        if user_latitude and user_longitude:
            user_location = {'latitude': user_latitude, 'longitude': user_longitude}
        
        recommendations = ai_classifier.get_disposal_recommendations(
            classification_result, user_location
        )
        
        # Build response
        response_data = {
            'id': waste_item_id,
            'identified_type': classification_result.get('identified_type'),
            'confidence_score': classification_result.get('confidence_score', 0.0),
            'material_category': classification_result.get('material_category'),
            'recyclable': classification_result.get('recyclable', False),
            'disposal_method': classification_result.get('disposal_method'),
            'preparation_tips': classification_result.get('preparation_tips'),
            'environmental_impact': recommendations.get('environmental_impact'),
            'alternatives': recommendations.get('alternatives', []),
            'image_path': f'/static/{os.path.relpath(image_path, os.path.join(os.path.dirname(__file__), "..", "static"))}',
            'recommended_center': recommended_center
        }
        
        return jsonify({
            'success': True,
            'data': response_data,
            'message': 'Waste identified successfully'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Classification failed: {str(e)}'
        }), 500

@waste_identification_bp.route('/waste-history/<int:user_id>', methods=['GET'])
def get_waste_history(user_id):
    """Get waste identification history for a user."""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        # Query waste items for the user
        waste_items = WasteItem.query.filter_by(user_id=user_id)\
                                   .order_by(WasteItem.created_at.desc())\
                                   .paginate(page=page, per_page=per_page, error_out=False)
        
        # Format response
        items = []
        for item in waste_items.items:
            item_data = {
                'id': item.id,
                'identified_type': item.identified_type,
                'confidence_score': item.confidence_score,
                'material_category': item.material_category,
                'recyclable': item.recyclable,
                'disposal_method': item.disposal_method,
                'image_path': item.image_path,
                'created_at': item.created_at.isoformat(),
            }
            
            # Add recommended center info if available
            if item.recommended_center_id:
                center = RecyclingCenter.query.get(item.recommended_center_id)
                if center:
                    item_data['recommended_center'] = {
                        'id': center.id,
                        'name': center.name,
                        'address': center.address
                    }
            
            items.append(item_data)
        
        return jsonify({
            'success': True,
            'data': items,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': waste_items.total,
                'pages': waste_items.pages,
                'has_next': waste_items.has_next,
                'has_prev': waste_items.has_prev
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@waste_identification_bp.route('/waste-stats/<int:user_id>', methods=['GET'])
def get_waste_stats(user_id):
    """Get waste statistics for a user."""
    try:
        # Get all waste items for the user
        waste_items = WasteItem.query.filter_by(user_id=user_id).all()
        
        total_scanned = len(waste_items)
        recyclable_count = sum(1 for item in waste_items if item.recyclable)
        non_recyclable_count = total_scanned - recyclable_count
        
        # Category breakdown
        category_breakdown = {}
        for item in waste_items:
            category = item.material_category or 'unknown'
            category_breakdown[category] = category_breakdown.get(category, 0) + 1
        
        # Recent activity (last 30 days)
        from datetime import datetime, timedelta
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        recent_items = [item for item in waste_items if item.created_at >= thirty_days_ago]
        recent_activity_30_days = len(recent_items)
        
        # Calculate recycling rate
        recycling_rate = (recyclable_count / total_scanned * 100) if total_scanned > 0 else 0
        
        return jsonify({
            'success': True,
            'data': {
                'total_scanned': total_scanned,
                'recyclable_count': recyclable_count,
                'non_recyclable_count': non_recyclable_count,
                'category_breakdown': category_breakdown,
                'recent_activity_30_days': recent_activity_30_days,
                'recycling_rate': round(recycling_rate, 2)
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@waste_identification_bp.route('/waste-categories', methods=['GET'])
def get_waste_categories():
    """Get information about supported waste categories."""
    try:
        categories = ai_classifier.waste_categories
        
        return jsonify({
            'success': True,
            'data': categories
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
