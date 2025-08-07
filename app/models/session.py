import uuid
from datetime import datetime
from app.extensions import db


class Session(db.Model):
    id = db.Column(db.String(36), primary_key=True,
                   default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=datetime.now)
    started = db.Column(db.Boolean, default=False)
    finished = db.Column(db.Boolean, default=False)
    
    players = db.relationship('Player', backref='session', lazy=True)