from app.extensions import db


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(150))

    def to_dict(self):
        return {
            "id": self.id,
            "text": self.text
        }
        
class SessionQuestion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String, db.ForeignKey("session.id"), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey("question.id"), nullable=False)
    order = db.Column(db.Integer, default=1, nullable=False)
    
    question = db.relationship("Question")
    
    def __init__(self, session_id: str, question_id: int, order:int) -> None:
        self.session_id = session_id
        self.question_id = question_id
        self.order = order