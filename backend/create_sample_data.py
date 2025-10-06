import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from src.main import app
from src.models.user import db, User
from src.models.recycling_center import RecyclingCenter
import json

def create_sample_data():
    with app.app_context():
        # Create sample users
        users_data = [
            {
                'username': 'john_doe',
                'email': 'john@example.com',
                'password_hash': 'hashed_password_123',
                'first_name': 'John',
                'last_name': 'Doe',
                'phone': '+1234567890',
                'address': '123 Main St, Chicago, IL',
                'latitude': 41.8781,
                'longitude': -87.6298,
                'user_type': 'household'
            },
            {
                'username': 'jane_picker',
                'email': 'jane@example.com',
                'password_hash': 'hashed_password_456',
                'first_name': 'Jane',
                'last_name': 'Smith',
                'phone': '+1234567891',
                'address': '456 Oak Ave, Chicago, IL',
                'latitude': 41.8825,
                'longitude': -87.6235,
                'user_type': 'wastepicker'
            }
        ]
        
        for user_data in users_data:
            existing_user = User.query.filter_by(email=user_data['email']).first()
            if not existing_user:
                user = User(**user_data)
                db.session.add(user)
        
        # Create sample recycling centers
        centers_data = [
            {
                'name': 'GreenCycle Recycling',
                'address': '789 Green St, Chicago, IL 60601',
                'latitude': 41.8819,
                'longitude': -87.6278,
                'phone': '+1234567892',
                'email': 'info@greencycle.com',
                'website': 'https://greencycle.com',
                'operating_hours': json.dumps({
                    'monday': '8:00-17:00',
                    'tuesday': '8:00-17:00',
                    'wednesday': '8:00-17:00',
                    'thursday': '8:00-17:00',
                    'friday': '8:00-17:00',
                    'saturday': '9:00-15:00',
                    'sunday': 'closed'
                }),
                'accepted_materials': json.dumps(['plastic', 'paper', 'glass', 'metal']),
                'special_instructions': 'Please clean all containers before drop-off',
                'rating': 4.5,
                'total_reviews': 128
            },
            {
                'name': 'Central Waste Solutions',
                'address': '321 Recycle Blvd, Chicago, IL 60602',
                'latitude': 41.8756,
                'longitude': -87.6244,
                'phone': '+1234567893',
                'email': 'contact@centralwaste.com',
                'website': 'https://centralwaste.com',
                'operating_hours': json.dumps({
                    'monday': '7:00-18:00',
                    'tuesday': '7:00-18:00',
                    'wednesday': '7:00-18:00',
                    'thursday': '7:00-18:00',
                    'friday': '7:00-18:00',
                    'saturday': '8:00-16:00',
                    'sunday': '10:00-14:00'
                }),
                'accepted_materials': json.dumps(['plastic', 'paper', 'glass', 'metal', 'electronics']),
                'special_instructions': 'Electronics accepted on weekends only',
                'rating': 4.2,
                'total_reviews': 89
            },
            {
                'name': 'EcoHub Recycling Center',
                'address': '555 Earth Way, Chicago, IL 60603',
                'latitude': 41.8892,
                'longitude': -87.6189,
                'phone': '+1234567894',
                'email': 'hello@ecohub.com',
                'website': 'https://ecohub.com',
                'operating_hours': json.dumps({
                    'monday': '9:00-16:00',
                    'tuesday': '9:00-16:00',
                    'wednesday': '9:00-16:00',
                    'thursday': '9:00-16:00',
                    'friday': '9:00-16:00',
                    'saturday': '10:00-15:00',
                    'sunday': 'closed'
                }),
                'accepted_materials': json.dumps(['plastic', 'paper', 'organic', 'hazardous']),
                'special_instructions': 'Hazardous waste by appointment only',
                'rating': 4.8,
                'total_reviews': 203
            }
        ]
        
        for center_data in centers_data:
            existing_center = RecyclingCenter.query.filter_by(name=center_data['name']).first()
            if not existing_center:
                center = RecyclingCenter(**center_data)
                db.session.add(center)
        
        db.session.commit()
        print('Sample data created successfully!')

if __name__ == '__main__':
    create_sample_data()
