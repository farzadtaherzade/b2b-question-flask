from flask import Blueprint, jsonify

bp = Blueprint("errors", __name__)

@bp.app_errorhandler(404)
def not_found(error):
    return jsonify({"error": error.description}), 404

@bp.app_errorhandler(500)
def internal_server_error(error):
    return {
        "error": "Internal Server Error",
        "message": "An unexpected error occurred. Please try again later."
    }, 500
