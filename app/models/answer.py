from app.extensions import db


class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey(
        "session_question.id"), nullable=False)
    answer = db.Column(db.String(3), nullable=False)
    session_id = db.Column(db.String, db.ForeignKey("session.id"), nullable=False)
    player_id = db.Column(db.Integer, db.ForeignKey("player.id"), nullable=False)