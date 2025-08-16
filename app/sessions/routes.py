from app.sessions import bp
from app.models.session import Session
from app.models.question import Question, SessionQuestion
from app.models.player import Player
from app.models.answer import Answer
from flask import request, jsonify
from app.models.schema import session_schema, questions_schema, session_questions_schema, players_schema, answer_questions_schema
from app.extensions import db
from sqlalchemy.sql.expression import func
from marshmallow import ValidationError

from app.tasks import ended_session


@bp.route("/session/create", methods=["POST"])
def create_session():
    try:
        data = request.get_json()
    except ValidationError as err:
        return jsonify({
            "error": err.messages
        }), 400
    username = data.get("username")

    if not username:
        return jsonify({"errors": {
            "username": "Is Required"
        }})

    session = Session()
    db.session.add(session)
    db.session.commit()

    player = Player(
        username=username.lower(),
        session_id=session.id,
        is_leader=True,
        is_ready=True
    )
    db.session.add(player)
    db.session.commit()

    return {"message": "Session created",
            "session_room": session_schema.dump(session),
            "player_id": player.id
            }, 201


@bp.route("/session/<string:id>/status", methods=["GET"])
def session_status(id):
    session = Session.query.get_or_404(id)

    return jsonify({
        "session_room": session_schema.dump(session),
        "players": players_schema.dump(session.players)
    }), 200


@bp.route("/session/<string:id>/join", methods=["POST"])
def join_session(id):
    session = Session.query.get_or_404(id)

    if len(session.players) >= 2:
        return jsonify({
            "errors": {
                "players": "lobby is full max is 2",
                "action": "LOBBY_FULL"
            }
        }), 400

    data = request.get_json()
    username = data.get("username")
    if not data and not data.get("username"):
        return jsonify({"errors": {
            "username": "Is Required",
            "action":"USERNAME_REQUIRED"
        }}), 400
    # cb20efeb-88e7-4a56-b1d2-f15c027c27c7
    username_exists = Player.query.filter_by(
        username=data.get("username").lower(),
        session_id=session.id
    ).first()

    if username_exists:
        return jsonify({"errors": {
            "username": "Username is in the game try another username",
            "action": "DUPLICATE_USERNAME"
        }}), 400

    player = Player(
        username=username,
        session_id=session.id
    )
    db.session.add(player)
    db.session.commit()
    return jsonify({"message": "You Joined the match"})


@bp.route("/session/<string:id>/start", methods=["POST"])
def start_game(id):
    session = Session.query.get_or_404(id)
    data = request.get_json()

    player_id = data.get("player_id")
    if not player_id:
        return jsonify({
            "errors": {
                "player_id": "player_id is required"
            }
        }), 400

    player = next((p for p in session.players if p.id == player_id), None)
    if not player:
        return jsonify({
            "errors": {
                "player_id": "Player not found in this session"
            }
        }), 400

    if not player.is_leader:
        return jsonify({
            "errors": {
                "permission": "Only the leader can start the game"
            }
        }), 403

    if session.started:
        session_question = SessionQuestion.query.filter_by(
            session_id=session.id)
        return jsonify({
            "questions": session_questions_schema.dump(session_question)
        }), 200

    if not session.players[0].is_ready or not session.players[1].is_ready:
        return jsonify({
            "errors": {
                "players": "Players not ready",
            },
        }), 400
    questions = Question.query.order_by(func.random()).limit(10).all()
    ret = []
    for index, question in enumerate(questions, start=1):
        session_question = SessionQuestion(
            session_id=session.id,
            question_id=question.id,
            order=index
        )
        ret.append(session_question)
        db.session.add(session_question)

    session.started = True
    db.session.add(session)
    db.session.commit()
    ended_session.apply_async(args=[session.id], countdown=70)  # type: ignore
    return jsonify({
        "questions": session_questions_schema.dump(ret),
    })


@bp.route("/session/<string:id>/ready", methods=["POST"])
def ready_player(id):
    data = request.get_json()
    username = data.get("username").lower()

    if not data and not username:
        return jsonify({
            "errors": {
                "username": "Username is required"
            }
        }), 400

    print(username)
    print(id)
    
    player = Player.query.filter_by(
        username=username, session_id=id).first_or_404()
    player.is_ready = True
    db.session.add(player)
    db.session.commit()
    return jsonify({
        "message": f"{username} is ready"
    }), 200


@bp.route("/session/<string:session_id>/result", methods=["GET"])
def result(session_id):
    session = Session.query.get_or_404(session_id)
    if not session.finished:
        return jsonify({
            "message": "game is not finisehd yet!"
        }), 400
    qeustions = SessionQuestion.query.filter_by(session_id=session_id).all()

    answers_player_1 = Answer.query.filter_by(
        session_id=session_id, player_id=session.players[0].id).all()
    answers_player_2 = Answer.query.filter_by(
        session_id=session_id, player_id=session.players[1].id).all()
    return jsonify(
        {
            "data": {
                "player_1": {
                    "answers": answer_questions_schema.dump(answers_player_1) if answers_player_1 else [],
                    "score": len(answers_player_1),
                },
                "player_2": {
                    "answers": answer_questions_schema.dump(answers_player_2) if answers_player_2 else [],
                    "score": len(answers_player_2),
                }
            },
            "questions": session_questions_schema.dump(qeustions),
        }
    ), 200
