from app.models.question import Question, SessionQuestion
from app.models.session import Session
from app.models.answer import Answer
from app.models.player import Player
from marshmallow import fields, validates, ValidationError
from app.extensions import ma

class PlayerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Player
        load_instance = True
        include_fk = True

players_schema = PlayerSchema(many=True)

class SessionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Session
        load_instance = True
        include_fk = True
    
    players = ma.Nested(PlayerSchema) # type: ignore

session_schema = SessionSchema()
sessions_schema = SessionSchema(many=True)


class QuestionSchema(ma.Schema):
    text = fields.Str(required=True)

    @validates("text")
    def validate_text(self, value, **kwargs):
        if not value.strip():
            raise ValidationError("Question text cannot be empty")
        if len(value) > 500:
            raise ValidationError("Question text cannot exceed 500 characters")
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