from flask import Flask
from config import Config
from app.extensions import db, ma, migrate, jwt
from dotenv import load_dotenv
from faker import Faker
from app.celery_app import celery_init_app

load_dotenv()
faker = Faker()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize Flask extensions
    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)
    celery_init_app(app)
    jwt.init_app(app)

    # register blueprints
    from app.main import bp as main_bp
    from app.questions import question_bp
    from app.sessions import bp as session_bp
    from app.users import bp as users_bp
    from app.errors import bp as error_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(question_bp)
    app.register_blueprint(session_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(error_bp) # register error handling blueprint

    @app.cli.command("seed")
    def seed():
        from app.models.question import Question

        questions = [Question(text=faker.sentence()) for _ in range(10)] # type: ignore

        db.session.add_all(questions)   # ✅ Add this line
        db.session.commit()             # ✅ And this line

        print("✅ Seeded 10 random questions.")    
    
    return app