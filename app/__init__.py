from flask import Flask, jsonify
from config import Config
from app.extensions import db
from dotenv import load_dotenv
load_dotenv()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize Flask extensions
    db.init_app(app)

    # register blueprints
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    with app.app_context():
        from app.models.answer import Answer
        from app.models.question import Question
        from app.models.session import Session

        db.create_all()

    return app
