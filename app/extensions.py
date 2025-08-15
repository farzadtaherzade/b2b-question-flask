from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
import redis
from flask_socketio import SocketIO
from flask_cors import CORS

client = redis.Redis("localhost", port=6379)

db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()
jwt = JWTManager()
socket = SocketIO(cors_allowed_origins="*")
cors = CORS()
