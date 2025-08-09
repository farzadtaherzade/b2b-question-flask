from app.extensions import client


def get_auth_code(user_id):
    value = client.get(f"code:{user_id}")
    return value.decode("utf-8") if value else None # type: ignore


def set_auth_code(code, user_id):
    return client.setex(f"code:{user_id}", 60 * 3, code)

def remove_auth_code(user_id):
    return client.delete(f"code:{user_id}")

def update_user_score(score, username):
    return client.zincrby("leaderboard", score, username)