from flask import Blueprint

question_bp = Blueprint("question", __name__)

from app.questions import routes