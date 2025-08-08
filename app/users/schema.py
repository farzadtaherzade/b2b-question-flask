from app.models.users import User
from marshmallow import fields, validates, ValidationError
from app.extensions import ma

class AuthSendCodeSchema(ma.Schema):
    email = ma.Email() # type: ignore

auth_send_code_schema = AuthSendCodeSchema()


class VerifyOtpSchema(ma.Schema):
    email = fields.Email(required=True)
    code = fields.Integer(required=True)

    @validates("code")
    def validate_code(self, value, data_key, **kwargs):
        if not (10000 <= value <= 99999):
            raise ValidationError("Code must be a 5-digit number between 10000 and 99999.")
verify_otp_schema = VerifyOtpSchema()

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
    
    id = ma.auto_field() # type: ignore
    username =ma.auto_field() # type: ignore
    created_at = ma.auto_field()     # type: ignore
    email = ma.auto_field()     # type: ignore
    
user_schema = UserSchema()