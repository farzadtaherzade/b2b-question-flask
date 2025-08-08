from flask import request, jsonify
from app.users import bp
from app.models.users import User
from app.extensions import db
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from app.users.schema import auth_send_code_schema, verify_otp_schema, user_schema
from random import randint
from app.services.redis_service import get_auth_code, set_auth_code, remove_auth_code


@bp.route("/auth/send_otp",methods=["POST"])
def send_otp():
    json = request.get_json()
    if not json:
        return jsonify({"error": "Invalid JSON"}), 400
    data = auth_send_code_schema.load(json)

    user_exists = User.query.filter_by(
        email=data["email"]).first()  # type: ignore
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
            "code": code,  # ! temparary
            "message": "OTP code sent successfully"
        }), 200

    user = User(email=data.get("email"))  # type: ignore
    db.session.add(user)
    db.session.commit()
    token = randint(10000, 99999)
    set_auth_code(token, user.id)
    # TODO sending async email for otp code

    return jsonify({
        "token": token,  # ! temparary
        "message": "OTP code sent successfully"
    }), 200


@bp.route("/auth/verify", methods=["POST"])
def verify_otp():
    json = request.get_json()
    if not json:
        return jsonify({"error": "Invalid JSON"}), 400

    
    data = verify_otp_schema.load(json)
    user = User.query.filter_by(email=data.get("email")).first()  # type: ignore
    if not user:
        return jsonify({
            "error": "User not found"
        }), 400
    token = get_auth_code(user.id)

    print(token, type(token))
    if not token or str(token) != str(data.get("code")): # type: ignore
        return jsonify({"error": "Invalid or expired OTP"}), 400

    access_token = create_access_token(identity=user.email)
    remove_auth_code(user.id)
    return jsonify({
        "access_token": access_token
    }), 200


@bp.route("/me", methods=["GET"])
@jwt_required()
def me():
    payload = get_jwt_identity()
    user = User.query.filter_by(email=payload).first()
    return jsonify(user_schema.dump(user))