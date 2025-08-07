from app.models.users import User
from marshmallow import fields, validates, ValidationError
from app.extensions import ma

class AuthSendCodeSchema(ma.Schema):
    email = ma.Email()
    
auth_send_code_schema = AuthSendCodeSchema()

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
    
    id = ma.auto_field()
    username =ma.auto_field()
    created_at = ma.auto_field()    
    email = ma.auto_field()    