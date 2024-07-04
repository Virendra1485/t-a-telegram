import os
import random
import requests
from datetime import datetime, timedelta
from flask import request
from flask_restful import Resource
from marshmallow import ValidationError
from .models import User, Otp
from .schema import UserRegisterRequestSchema
from extensions import db


class UserCreateApi(Resource):
    def post(self):
        schema = UserRegisterRequestSchema()
        try:
            data = schema.load(request.json)
        except ValidationError as err:
            return err.messages, 400
        db.session.add(data)
        db.session.commit()
        return {"message": "User Created successfully !"}


class LoginApi(Resource):
    def post(self):
        data = request.get_json()
        identifier = data.get('identifier')

        if not identifier:
            return {"message": "Identifier is required"}, 400

        user = User.query.filter((User.username == identifier) | (User.phone_number == identifier)).first()

        if not user:
            return {"message": "User not found"}, 404

        otp = random.randint(100000, 999999)
        new_otp = Otp(otp=str(otp), user_id=user.id)
        db.session.add(new_otp)
        db.session.commit()
        message = f"Your OTP is {otp}"

        # self.send_message_to_telegram(user.telegram_id, message)

        return {"message": "OTP sent to your Telegram number"}, 200

    @staticmethod
    def send_message_to_telegram(chat_id, text):

        url = f"https://api.telegram.org/bot{os.environ.get('TELEGRAM_TOKEN')}/sendMessage"
        payload = {'chat_id': chat_id, 'text': text}
        requests.post(url, data=payload)


class VerifyOtpApi(Resource):
    def post(self):
        data = request.get_json()
        identifier = data.get('identifier')
        otp = data.get('otp')

        if not identifier or not otp:
            return {"message": "Identifier and OTP are required"}, 400

        user = User.query.filter((User.username == identifier) | (User.phone_number == identifier)).first()

        if not user:
            return {"message": "User not found"}, 404

        latest_otp = Otp.query.filter_by(user_id=user.id, otp=otp).filter(
            Otp.created_at > datetime.now() - timedelta(minutes=15)).first()

        if not latest_otp:
            return {"message": "Invalid OTP !"}, 404

        latest_otp.expired = True
        db.session.add(latest_otp)
        db.session.commit()

        return {"message": "OTP verified successfully"}, 200
