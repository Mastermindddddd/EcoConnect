from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    phone = db.Column(db.String(20))
    address = db.Column(db.String(300))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    user_type = db.Column(db.String(20), default='household')  # household, wastepicker, admin
    is_active = db.Column(db.Boolean, default=True)
    profile_image = db.Column(db.String(300))
    total_recycled_weight = db.Column(db.Float, default=0.0)
    points = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def __repr__(self):
        return f'<User {self.username}>'

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'phone': self.phone,
            'address': self.address,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'user_type': self.user_type,
            'is_active': self.is_active,
            'profile_image': self.profile_image,
            'total_recycled_weight': self.total_recycled_weight,
            'points': self.points,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }