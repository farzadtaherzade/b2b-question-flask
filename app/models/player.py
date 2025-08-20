from app.extensions import db
from datetime import datetime

class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=False)
    session_id = db.Column(db.String, db.ForeignKey("session.id"), nullable=False)
    joined_at = db.Column(db.DateTime, default=datetime.now)
    is_ready = db.Column(db.Boolean, default=False)
    is_leader = db.Column(db.Boolean, default=False)
    notification_sended=db.Column(db.Boolean, default=False)
    
    __table_args__ = (
        db.UniqueConstraint("username", "session_id", name="player_session__id_username"),
    )
    
    def __init__(self, username:str, session_id: str, is_leader=False, is_ready=False) -> None:
        self.username = username
        self.session_id = session_id
        self.is_leader=is_leader
        self.is_ready = is_ready