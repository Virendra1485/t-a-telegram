from marshmallow import validate, validates, ValidationError
from extensions import ma
from .models import User


class UserRegisterRequestSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User
        load_instance = True

    first_name = ma.auto_field(required=True)
    last_name = ma.auto_field(required=True)
    username = ma.auto_field(required=True)
    email = ma.auto_field(required=True)
    phone_number = ma.auto_field(required=True, validate=validate.Length(min=10))

    @validates('phone_number')
    def validate_phone_number(self, value):
        if User.query.filter_by(phone_number=value).first():
            raise ValidationError('Phone number already exists')

    @validates('username')
    def validate_username(self, value):
        if User.query.filter_by(username=value).first():
            raise ValidationError('Username already exists')

    @validates('email')
    def validate_phone_number(self, value):
        if User.query.filter_by(email=value).first():
            raise ValidationError('Email already exists')
