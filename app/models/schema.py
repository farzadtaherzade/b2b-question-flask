from flask_marshmallow import Marshmallow
from app.models.question import Question, SessionQuestion
from app.models.session import Session
from app.models.answer import Answer
from app.models.player import Player
from marshmallow import fields, validates, ValidationError
from app.extensions import ma

class SessionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Session
        load_instance = True
        include_fk = True

session_schema = SessionSchema()
sessions_schema = SessionSchema(many=True)

class QuestionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Question
        load_instance = True
        include_fk = True

    text = fields.Str(required=True, validate=lambda x: 0 < len(x) <= 150)

    @validates('text')
    def validate_text(self, value):
        if not value.strip():
            raise ValidationError('Question text cannot be empty or just whitespace.')

question_schema = QuestionSchema()
questions_schema = QuestionSchema(many=True)

class SessionQuestionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = SessionQuestion
        load_instance = True
        include_fk = True
    
    question = ma.Nested(QuestionSchema) # type: ignore
    
session_questions_schema = SessionQuestionSchema(many=True)


class AnswerQuestionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Answer
        load_instance = True
        include_fk = True
        
    answer = fields.Str(required=True, validate=lambda x: x.lower() in ["yes", "no"])

answer_question_schema = AnswerQuestionSchema()
answer_questions_schema = AnswerQuestionSchema(many=True)