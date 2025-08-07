from flask import Blueprint, jsonify

bp = Blueprint("errors", __name__)

@bp.app_errorhandler(404)
def not_found(error):
    return jsonify({"error": error.description}), 404