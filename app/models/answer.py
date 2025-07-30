from app.extensions import db


class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey(
        "question.id"), nullable=False)
    answer = db.Column(db.String(3), nullable=False)
