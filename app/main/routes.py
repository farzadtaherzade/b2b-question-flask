from app.main import bp
from flask import jsonify
from app.extensions import client


@bp.route("/")
def index():
    return jsonify({"message": "index page"})

@bp.route("/leaderboard")
def leaderboard():
    leaderboard = client.zrevrange("leaderboard", 0, 9, withscores=True)
    result = []
    for rank, (username, score) in enumerate(leaderboard, start=1): # type: ignore
        result.append({
            "rank": rank,
            "username": username.decode("utf-8"),  # Redis returns bytes
            "score": int(score)  # Convert float to int if needed
        })
    return jsonify({
        "leaderboard": result
    })
