# models.py
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    farm_location = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<User {self.username}>'

class FarmData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    soil_type = db.Column(db.String(50))
    crop_type = db.Column(db.String(50))
    area = db.Column(db.Float)
    irrigation_type = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class CropRecommendation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    crop_name = db.Column(db.String(50))
    soil_type = db.Column(db.String(50))
    season = db.Column(db.String(20))
    water_need = db.Column(db.String(20))
    yield_estimate = db.Column(db.String(50))
    recommended_at = db.Column(db.DateTime, default=datetime.utcnow)

class DiseaseDetection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    image_path = db.Column(db.String(200))
    detected_disease = db.Column(db.String(100))
    confidence_score = db.Column(db.Float)
    treatment_recommendation = db.Column(db.Text)
    detected_at = db.Column(db.DateTime, default=datetime.utcnow)