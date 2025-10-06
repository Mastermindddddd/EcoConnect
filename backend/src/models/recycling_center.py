from src.models.user import db

class RecyclingCenter(db.Model):
    __tablename__ = 'recycling_centers'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    address = db.Column(db.String(300), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    phone = db.Column(db.String(20))
    email = db.Column(db.String(120))
    website = db.Column(db.String(200))
    operating_hours = db.Column(db.Text)  # JSON string for flexible hours
    accepted_materials = db.Column(db.Text)  # JSON string for material types
    special_instructions = db.Column(db.Text)
    rating = db.Column(db.Float, default=0.0)
    total_reviews = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def __repr__(self):
        return f'<RecyclingCenter {self.name}>'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'address': self.address,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'phone': self.phone,
            'email': self.email,
            'website': self.website,
            'operating_hours': self.operating_hours,
            'accepted_materials': self.accepted_materials,
            'special_instructions': self.special_instructions,
            'rating': self.rating,
            'total_reviews': self.total_reviews,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
