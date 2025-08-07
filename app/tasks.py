from celery import shared_task
from app.extensions import db

@shared_task()
def ended_session(session_id):
    from app.models.session import Session
    
    session = Session.query.get(session_id)
    if session and not session.finished:
        session.finished = True
        db.session.add(session)
        db.session.commit()
        print(f"session ended after 70 seconds with id {session_id}.")
    print(f"session with id {session_id} does not exist!")