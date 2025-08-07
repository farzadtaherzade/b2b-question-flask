from flask import request, jsonify
from app.users import bp
from app.models.users import User
from app.extensions import db
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from app.users.schema import auth_send_code_schema
from random import randint
from app.services.redis_service import get_auth_code, set_auth_code


@bp.route("/auth/send_otp")
def send_otp():
    json_data = request.get_json()
    if not json_data:
        return jsonify({"error": "Invalid JSON"}), 400
    data = auth_send_code_schema.load(json_data)

    user_exists = User.query.filter_by(email=data["email"]).first() # type: ignore
    if user_exists:
        old_code = get_auth_code(user_exists.id)

        if old_code:
            return jsonify({
                "message": "code already send to you! please check your inbox",
                "action": "ALREADY_SENDED"
            }), 200
        code = randint(10000, 99999)
        set_auth_code(code, user_exists.id)
        # TODO sending async email for otp code 
        
        return jsonify({
            "code": code,
            "message": "OTP code sent successfully"
        }), 200

    return jsonify(), 201
