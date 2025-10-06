from src.models.user import db

class PickupRequest(db.Model):
    __tablename__ = 'pickup_requests'
    
    id = db.Column(db.Integer, primary_key=True)
    requester_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    wastepicker_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    pickup_address = db.Column(db.String(300), nullable=False)
    pickup_latitude = db.Column(db.Float, nullable=False)
    pickup_longitude = db.Column(db.Float, nullable=False)
    waste_description = db.Column(db.Text)
    waste_category = db.Column(db.String(50))  # recyclable, organic, mixed, hazardous
    estimated_weight = db.Column(db.Float)
    pickup_date = db.Column(db.DateTime)
    status = db.Column(db.String(20), default='pending')  # pending, accepted, in_progress, completed, cancelled
    special_instructions = db.Column(db.Text)
    payment_amount = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    # Relationships
    requester = db.relationship('User', foreign_keys=[requester_id], backref=db.backref('pickup_requests', lazy=True))
    wastepicker = db.relationship('User', foreign_keys=[wastepicker_id], backref=db.backref('assigned_pickups', lazy=True))

    def __repr__(self):
        return f'<PickupRequest {self.id} - {self.status}>'

    def to_dict(self):
        return {
            'id': self.id,
            'requester_id': self.requester_id,
            'wastepicker_id': self.wastepicker_id,
            'pickup_address': self.pickup_address,
            'pickup_latitude': self.pickup_latitude,
            'pickup_longitude': self.pickup_longitude,
            'waste_description': self.waste_description,
            'waste_category': self.waste_category,
            'estimated_weight': self.estimated_weight,
            'pickup_date': self.pickup_date.isoformat() if self.pickup_date else None,
            'status': self.status,
            'special_instructions': self.special_instructions,
            'payment_amount': self.payment_amount,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'requester': self.requester.to_dict() if self.requester else None,
            'wastepicker': self.wastepicker.to_dict() if self.wastepicker else None
        }