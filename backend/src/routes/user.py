from flask import Blueprint, request, jsonify, session
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
from src.models.user import db, User

user_bp = Blueprint('user', __name__)

@user_bp.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()
    
    required_fields = ['username', 'email', 'password']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'{field} is required'}), 400
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already exists'}), 400

    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username already exists'}), 400

    hashed_password = generate_password_hash(data['password'])
    user = User(
        username=data['username'],
        email=data['email'],
        password_hash=hashed_password,
        first_name=data.get('first_name'),
        last_name=data.get('last_name'),
        phone=data.get('phone'),
        address=data.get('address'),
        latitude=data.get('latitude'),
        longitude=data.get('longitude'),
        user_type=data.get('user_type', 'household')
    )
    
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully', 'user': user.to_dict()}), 201

@user_bp.route('/login', methods=['POST'])
def login_user():
    data = request.get_json()

    if not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Email and password are required'}), 400

    user = User.query.filter_by(email=data['email']).first()
    if not user or not check_password_hash(user.password_hash, data['password']):
        return jsonify({'error': 'Invalid email or password'}), 401

    # Create a session
    session['user_id'] = user.id
    session['username'] = user.username

    return jsonify({'message': 'Login successful', 'user': user.to_dict()}), 200


@user_bp.route('/logout', methods=['POST'])
def logout_user():
    session.clear()
    return jsonify({'message': 'Logged out successfully'}), 200



@user_bp.route('/session', methods=['GET'])
def get_session():
    """Check if user is still logged in"""
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        if user:
            return jsonify({
                'logged_in': True,
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'username': user.username
                }
            })
    return jsonify({'logged_in': False}), 200

