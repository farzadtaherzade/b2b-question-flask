from marshmallow import ValidationError
from app.questions import question_bp as bp
from flask import jsonify, request
from app.models.question import Question, SessionQuestion
from app.models.answer import Answer
from app.extensions import db, socket
from sqlalchemy.sql.expression import func
from app.models.session import Session
from app.models.schema import answer_question_schema, question_schema
from flask_jwt_extended import jwt_required
from app.tasks import handle_questions_finished


@bp.route("/question", methods=["GET"])
def index():
    questions = Question.query.order_by(func.random()).limit(10).all()

    return jsonify({
        "questions": [
            q.to_dict()
            for q in questions
        ]
    })


@bp.route("/question/answer", methods=["POST"])
def answer_question():
    try:
        data = answer_question_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify({"error": err.messages}), 400

    session = Session.query.get(data.session_id)
    if not session:
        return jsonify({"error": "Session not found"}), 404

    if session.finished:
        return jsonify({"error": "Session has already finished"}), 400

    player = next((p for p in session.players if p.id == data.player_id), None)
    if not player:
        return jsonify({"error": "Player not found in session"}), 404

    question = SessionQuestion.query.filter_by(
        session_id=data.session_id,
        question_id=data.question_id
    ).first()
    if not question:
        return jsonify({"error": "Question not found"}), 404

    # Optional: prevent duplicate answers
    existing_answer = Answer.query.filter_by(
        question_id=data.question_id,
        session_id=data.session_id,
        player_id=data.player_id
    ).first()

    if existing_answer:
        return jsonify({"error": "Player has already answered this question"}), 400
    answer = Answer(
        session_id=data.session_id,
        player_id=data.player_id,
        question_id=data.question_id,
        answer=data.answer
    )
    db.session.add(answer)
    db.session.commit()

    print("print_order", question.order,
          "question order", "question.id", question.id)
    if question.order == 20:
        answer_count = Answer.query.filter_by(
            session_id=data.session_id).count()
        print(answer_count, "answer_count -- ---- --- -")
        if answer_count == 40:
            handle_questions_finished.delay(data.session_id)  # type: ignore

        socket.emit("question_finished", {
                    "msg": f"{player.username} finish the questions"}, to=data.session_id)

    return jsonify({
        "message": "Answer submitted successfully",
        "answer": answer_question_schema.dump(data)
    }), 201


@bp.route("/questions/create", methods=["POST"])
@jwt_required()
def create_question():
    try:
        json_data = request.get_json()
        if not json_data:
            return jsonify({"error": "No input data provided"}), 400

        data = question_schema.load(json_data)  # validates 'text'
    except ValidationError as err:
        return jsonify(err.messages), 400

    new_question = Question(text=data["text"])  # type: ignore
    db.session.add(new_question)
    db.session.commit()

    return jsonify({
        "message": "Question created successfully",
        "question": question_schema.dump(new_question)
    }), 201
