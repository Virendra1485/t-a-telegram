from utils.models import BaseModel
from extensions import db


class User(BaseModel):
    __tablename__ = "users"

    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    email = db.Column(db.String(100), unique=True, nullable=False)
    username = db.Column(db.String(100), unique=True)
    phone_number = db.Column(db.String(20), unique=True)
    last_login = db.Column(db.DateTime, nullable=True)
    active = db.Column(db.Boolean, nullable=True)

    def __repr__(self):
        return f'<User {self.username}>'


class Otp(BaseModel):
    __tablename__ = "otps"

    otp = db.Column(db.String(6), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    expired = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<Otp {self.otp}>'
