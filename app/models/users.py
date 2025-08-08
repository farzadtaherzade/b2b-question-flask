from app.extensions import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    
    created_at = db.Column(db.DateTime, default=datetime.now)