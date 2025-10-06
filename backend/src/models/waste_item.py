from src.models.user import db

class WasteItem(db.Model):
    __tablename__ = 'waste_items'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    image_path = db.Column(db.String(300))
    identified_type = db.Column(db.String(100), nullable=False)
    confidence_score = db.Column(db.Float)
    material_category = db.Column(db.String(50))  # plastic, paper, glass, metal, organic, hazardous
    recyclable = db.Column(db.Boolean, default=True)
    disposal_method = db.Column(db.String(200))
    recommended_center_id = db.Column(db.Integer, db.ForeignKey('recycling_centers.id'))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    # Relationships
    user = db.relationship('User', backref=db.backref('waste_items', lazy=True))
    recommended_center = db.relationship('RecyclingCenter', backref=db.backref('recommended_items', lazy=True))

    def __repr__(self):
        return f'<WasteItem {self.identified_type}>'

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'image_path': self.image_path,
            'identified_type': self.identified_type,
            'confidence_score': self.confidence_score,
            'material_category': self.material_category,
            'recyclable': self.recyclable,
            'disposal_method': self.disposal_method,
            'recommended_center_id': self.recommended_center_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'recommended_center': self.recommended_center.to_dict() if self.recommended_center else None
        }
