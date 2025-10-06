from flask import Blueprint, request, jsonify
from src.models.user import db
from src.models.recycling_center import RecyclingCenter
import json
import math

recycling_centers_bp = Blueprint('recycling_centers', __name__)

def calculate_distance(lat1, lon1, lat2, lon2):
    """Calculate the great circle distance between two points on the earth (specified in decimal degrees)"""
    # Convert decimal degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    
    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    r = 6371  # Radius of earth in kilometers
    return c * r

@recycling_centers_bp.route('/recycling-centers', methods=['GET'])
def get_recycling_centers():
    """Get all recycling centers with optional filtering and location-based sorting"""
    try:
        # Get query parameters
        latitude = request.args.get('latitude', type=float)
        longitude = request.args.get('longitude', type=float)
        material_type = request.args.get('material_type')
        radius = request.args.get('radius', default=50, type=float)  # Default 50km radius
        limit = request.args.get('limit', default=20, type=int)
        
        # Base query
        query = RecyclingCenter.query.filter_by(is_active=True)
        
        # Get all centers
        centers = query.all()
        
        # Convert to dict and add distance if location provided
        centers_data = []
        for center in centers:
            center_dict = center.to_dict()
            
            # Parse accepted materials for filtering
            if center.accepted_materials:
                try:
                    accepted_materials = json.loads(center.accepted_materials)
                    center_dict['accepted_materials'] = accepted_materials
                except json.JSONDecodeError:
                    center_dict['accepted_materials'] = []
            else:
                center_dict['accepted_materials'] = []
            
            # Parse operating hours
            if center.operating_hours:
                try:
                    operating_hours = json.loads(center.operating_hours)
                    center_dict['operating_hours'] = operating_hours
                except json.JSONDecodeError:
                    center_dict['operating_hours'] = {}
            else:
                center_dict['operating_hours'] = {}
            
            # Calculate distance if user location provided
            if latitude and longitude:
                distance = calculate_distance(latitude, longitude, center.latitude, center.longitude)
                center_dict['distance'] = round(distance, 2)
                
                # Filter by radius
                if distance <= radius:
                    centers_data.append(center_dict)
            else:
                centers_data.append(center_dict)
        
        # Filter by material type if specified
        if material_type:
            centers_data = [
                center for center in centers_data
                if material_type.lower() in [material.lower() for material in center['accepted_materials']]
            ]
        
        # Sort by distance if location provided
        if latitude and longitude:
            centers_data.sort(key=lambda x: x.get('distance', float('inf')))
        
        # Limit results
        centers_data = centers_data[:limit]
        
        return jsonify({
            'success': True,
            'data': centers_data,
            'total': len(centers_data)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@recycling_centers_bp.route('/recycling-centers/<int:center_id>', methods=['GET'])
def get_recycling_center(center_id):
    """Get a specific recycling center by ID"""
    try:
        center = RecyclingCenter.query.get_or_404(center_id)
        center_dict = center.to_dict()
        
        # Parse JSON fields
        if center.accepted_materials:
            try:
                center_dict['accepted_materials'] = json.loads(center.accepted_materials)
            except json.JSONDecodeError:
                center_dict['accepted_materials'] = []
        
        if center.operating_hours:
            try:
                center_dict['operating_hours'] = json.loads(center.operating_hours)
            except json.JSONDecodeError:
                center_dict['operating_hours'] = {}
        
        return jsonify({
            'success': True,
            'data': center_dict
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@recycling_centers_bp.route('/recycling-centers', methods=['POST'])
def create_recycling_center():
    """Create a new recycling center (admin only)"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'address', 'latitude', 'longitude']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'error': f'Missing required field: {field}'
                }), 400
        
        # Create new center
        center = RecyclingCenter(
            name=data['name'],
            address=data['address'],
            latitude=data['latitude'],
            longitude=data['longitude'],
            phone=data.get('phone'),
            email=data.get('email'),
            website=data.get('website'),
            operating_hours=json.dumps(data.get('operating_hours', {})),
            accepted_materials=json.dumps(data.get('accepted_materials', [])),
            special_instructions=data.get('special_instructions')
        )
        
        db.session.add(center)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': center.to_dict(),
            'message': 'Recycling center created successfully'
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@recycling_centers_bp.route('/recycling-centers/<int:center_id>', methods=['PUT'])
def update_recycling_center(center_id):
    """Update a recycling center (admin only)"""
    try:
        center = RecyclingCenter.query.get_or_404(center_id)
        data = request.get_json()
        
        # Update fields
        if 'name' in data:
            center.name = data['name']
        if 'address' in data:
            center.address = data['address']
        if 'latitude' in data:
            center.latitude = data['latitude']
        if 'longitude' in data:
            center.longitude = data['longitude']
        if 'phone' in data:
            center.phone = data['phone']
        if 'email' in data:
            center.email = data['email']
        if 'website' in data:
            center.website = data['website']
        if 'operating_hours' in data:
            center.operating_hours = json.dumps(data['operating_hours'])
        if 'accepted_materials' in data:
            center.accepted_materials = json.dumps(data['accepted_materials'])
        if 'special_instructions' in data:
            center.special_instructions = data['special_instructions']
        if 'is_active' in data:
            center.is_active = data['is_active']
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': center.to_dict(),
            'message': 'Recycling center updated successfully'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@recycling_centers_bp.route('/recycling-centers/<int:center_id>', methods=['DELETE'])
def delete_recycling_center(center_id):
    """Delete a recycling center (admin only)"""
    try:
        center = RecyclingCenter.query.get_or_404(center_id)
        
        # Soft delete - just mark as inactive
        center.is_active = False
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Recycling center deleted successfully'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
