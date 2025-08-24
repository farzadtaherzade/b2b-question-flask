from celery import shared_task
from app.extensions import db
from app.services import redis_service

@shared_task()
def ended_session(session_id):
    from app.models.session import Session
    
    session = Session.query.get(session_id)
    if session and not session.finished:
        session.finished = True
        db.session.add(session)
        db.session.commit()
        handle_leaderboard.delay(session_id) # type: ignore
        return f"session ended after 70 seconds with id {session_id}."
    return f"session with id {session_id} is already finished! ---- ended_session task"
    
@shared_task()
def handle_leaderboard(session_id):
    from app.models.session import Session
    from app.models.answer import Answer
    session = Session.query.get(session_id)
    if session and session.finished:
        player_1_score = Answer.query.filter_by(session_id=session_id, player_id=session.players[0].id).count()
        player_2_score = Answer.query.filter_by(session_id=session_id, player_id=session.players[1].id).count()
        redis_service.update_user_score(player_1_score, session.players[0].username)
        redis_service.update_user_score(player_2_score, session.players[1].username)

    return f"session with id {session_id} does not exist! --- handle_leaderboard task"    

@shared_task()
def handle_questions_finished(session_id):
    from app.models.session import Session
    session = Session.query.get(session_id)
    if session and not session.finished:
            session.finished = True
            db.session.add(session)
            db.session.commit()
            handle_leaderboard.delay(session_id) # type: ignore
            return f"session ended on 40 question answers with id {session_id}."
    return f"session with id {session_id} is already finished! ------ handle_questions_finished task"