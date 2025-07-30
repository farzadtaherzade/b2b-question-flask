from app.main import bp
from flask import jsonify

@bp.route("/")
def index():
	return jsonify({"message": "index page"})
