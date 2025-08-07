from app.extensions import client

def get_auth_code(user_id):
    return client.get(f"code:{user_id}")

def set_auth_code(code, user_id):
    return client.setex(f"code:{user_id}", 60 * 3, code)