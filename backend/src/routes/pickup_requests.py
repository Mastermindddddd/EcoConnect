from flask import Blueprint, request, jsonify
from src.models.user import db
from src.models.pickup_request import PickupRequest
from src.models.user import User
from datetime import datetime
import math

pickup_requests_bp = Blueprint('pickup_requests', __name__)

def calculate_distance(lat1, lon1, lat2, lon2):
    """Calculate the great circle distance between two points on the earth"""
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    r = 6371  # Radius of earth in kilometers
    return c * r

@pickup_requests_bp.route('/pickup-requests', methods=['POST'])
def create_pickup_request():
    """Create a new pickup request"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['requester_id', 'pickup_address', 'pickup_latitude', 'pickup_longitude']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'error': f'Missing required field: {field}'
                }), 400
        
        # Parse pickup date if provided
        pickup_date = None
        if 'pickup_date' in data:
            try:
                pickup_date = datetime.fromisoformat(data['pickup_date'].replace('Z', '+00:00'))
            except ValueError:
                return jsonify({
                    'success': False,
                    'error': 'Invalid pickup_date format. Use ISO format.'
                }), 400
        
        # Create new pickup request
        pickup_request = PickupRequest(
            requester_id=data['requester_id'],
            pickup_address=data['pickup_address'],
            pickup_latitude=data['pickup_latitude'],
            pickup_longitude=data['pickup_longitude'],
            waste_description=data.get('waste_description'),
            waste_category=data.get('waste_category'),
            estimated_weight=data.get('estimated_weight'),
            pickup_date=pickup_date,
            special_instructions=data.get('special_instructions'),
            payment_amount=data.get('payment_amount')
        )
        
        db.session.add(pickup_request)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': pickup_request.to_dict(),
            'message': 'Pickup request created successfully'
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@pickup_requests_bp.route('/pickup-requests', methods=['GET'])
def get_pickup_requests():
    """Get pickup requests with optional filtering"""
    try:
        # Get query parameters
        status = request.args.get('status')
        requester_id = request.args.get('requester_id', type=int)
        wastepicker_id = request.args.get('wastepicker_id', type=int)
        latitude = request.args.get('latitude', type=float)
        longitude = request.args.get('longitude', type=float)
        radius = request.args.get('radius', default=25, type=float)  # Default 25km radius
        limit = request.args.get('limit', default=50, type=int)
        
        # Build query
        query = PickupRequest.query
        
        if status:
            query = query.filter_by(status=status)
        if requester_id:
            query = query.filter_by(requester_id=requester_id)
        if wastepicker_id:
            query = query.filter_by(wastepicker_id=wastepicker_id)
        
        # Get requests
        requests = query.order_by(PickupRequest.created_at.desc()).limit(limit).all()
        
        # Convert to dict and add distance if location provided
        requests_data = []
        for req in requests:
            req_dict = req.to_dict()
            
            # Calculate distance if user location provided
            if latitude and longitude:
                distance = calculate_distance(
                    latitude, longitude, 
                    req.pickup_latitude, req.pickup_longitude
                )
                req_dict['distance'] = round(distance, 2)
                
                # Filter by radius
                if distance <= radius:
                    requests_data.append(req_dict)
            else:
                requests_data.append(req_dict)
        
        # Sort by distance if location provided
        if latitude and longitude:
            requests_data.sort(key=lambda x: x.get('distance', float('inf')))
        
        return jsonify({
            'success': True,
            'data': requests_data,
            'total': len(requests_data)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@pickup_requests_bp.route('/pickup-requests/<int:request_id>', methods=['GET'])
def get_pickup_request(request_id):
    """Get a specific pickup request"""
    try:
        pickup_request = PickupRequest.query.get_or_404(request_id)
        return jsonify({
            'success': True,
            'data': pickup_request.to_dict()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@pickup_requests_bp.route('/pickup-requests/<int:request_id>/accept', methods=['POST'])
def accept_pickup_request(request_id):
    """Accept a pickup request (wastepicker)"""
    try:
        data = request.get_json()
        wastepicker_id = data.get('wastepicker_id')
        
        if not wastepicker_id:
            return jsonify({
                'success': False,
                'error': 'Wastepicker ID is required'
            }), 400
        
        # Verify wastepicker exists and is active
        wastepicker = User.query.filter_by(
            id=wastepicker_id, 
            user_type='wastepicker', 
            is_active=True
        ).first()
        
        if not wastepicker:
            return jsonify({
                'success': False,
                'error': 'Invalid wastepicker ID'
            }), 400
        
        # Get the pickup request
        pickup_request = PickupRequest.query.get_or_404(request_id)
        
        if pickup_request.status != 'pending':
            return jsonify({
                'success': False,
                'error': 'Pickup request is not available for acceptance'
            }), 400
        
        # Accept the request
        pickup_request.wastepicker_id = wastepicker_id
        pickup_request.status = 'accepted'
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': pickup_request.to_dict(),
            'message': 'Pickup request accepted successfully'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@pickup_requests_bp.route('/pickup-requests/<int:request_id>/status', methods=['PUT'])
def update_pickup_status(request_id):
    """Update pickup request status"""
    try:
        data = request.get_json()
        new_status = data.get('status')
        
        if not new_status:
            return jsonify({
                'success': False,
                'error': 'Status is required'
            }), 400
        
        valid_statuses = ['pending', 'accepted', 'in_progress', 'completed', 'cancelled']
        if new_status not in valid_statuses:
            return jsonify({
                'success': False,
                'error': f'Invalid status. Must be one of: {", ".join(valid_statuses)}'
            }), 400
        
        pickup_request = PickupRequest.query.get_or_404(request_id)
        pickup_request.status = new_status
        
        # If completed, update user's recycled weight and points
        if new_status == 'completed' and pickup_request.estimated_weight:
            requester = User.query.get(pickup_request.requester_id)
            if requester:
                requester.total_recycled_weight += pickup_request.estimated_weight
                requester.points += int(pickup_request.estimated_weight * 10)  # 10 points per kg
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': pickup_request.to_dict(),
            'message': f'Pickup request status updated to {new_status}'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@pickup_requests_bp.route('/pickup-requests/<int:request_id>', methods=['DELETE'])
def cancel_pickup_request(request_id):
    """Cancel a pickup request"""
    try:
        pickup_request = PickupRequest.query.get_or_404(request_id)
        
        if pickup_request.status in ['completed', 'cancelled']:
            return jsonify({
                'success': False,
                'error': 'Cannot cancel a completed or already cancelled request'
            }), 400
        
        pickup_request.status = 'cancelled'
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Pickup request cancelled successfully'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@pickup_requests_bp.route('/wastepicker/<int:wastepicker_id>/stats', methods=['GET'])
def get_wastepicker_stats(wastepicker_id):
    """Get statistics for a wastepicker"""
    try:
        # Verify wastepicker exists
        wastepicker = User.query.filter_by(
            id=wastepicker_id, 
            user_type='wastepicker'
        ).first()
        
        if not wastepicker:
            return jsonify({
                'success': False,
                'error': 'Wastepicker not found'
            }), 404
        
        # Get pickup statistics
        total_pickups = PickupRequest.query.filter_by(wastepicker_id=wastepicker_id).count()
        completed_pickups = PickupRequest.query.filter_by(
            wastepicker_id=wastepicker_id, 
            status='completed'
        ).count()
        
        active_pickups = PickupRequest.query.filter_by(
            wastepicker_id=wastepicker_id, 
            status='in_progress'
        ).count()
        
        # Calculate total earnings (sum of payment amounts for completed pickups)
        earnings_result = db.session.query(
            db.func.sum(PickupRequest.payment_amount)
        ).filter_by(
            wastepicker_id=wastepicker_id, 
            status='completed'
        ).scalar()
        
        total_earnings = float(earnings_result) if earnings_result else 0.0
        
        # Calculate total weight collected
        weight_result = db.session.query(
            db.func.sum(PickupRequest.estimated_weight)
        ).filter_by(
            wastepicker_id=wastepicker_id, 
            status='completed'
        ).scalar()
        
        total_weight = float(weight_result) if weight_result else 0.0
        
        # Get recent activity (last 30 days)
        from datetime import datetime, timedelta
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        recent_pickups = PickupRequest.query.filter(
            PickupRequest.wastepicker_id == wastepicker_id,
            PickupRequest.created_at >= thirty_days_ago
        ).count()
        
        return jsonify({
            'success': True,
            'data': {
                'total_pickups': total_pickups,
                'completed_pickups': completed_pickups,
                'active_pickups': active_pickups,
                'total_earnings': total_earnings,
                'total_weight_collected': total_weight,
                'recent_activity_30_days': recent_pickups,
                'completion_rate': round((completed_pickups / total_pickups * 100), 2) if total_pickups > 0 else 0
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
