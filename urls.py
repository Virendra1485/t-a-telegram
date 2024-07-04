from flask import Blueprint
from flask_restful import Api
from user.routes import UserCreateApi, LoginApi, VerifyOtpApi

blueprint = Blueprint("/api", __name__, )
api = Api(blueprint)
api.add_resource(UserCreateApi, "/user")
api.add_resource(LoginApi, "/user/login")
api.add_resource(VerifyOtpApi, "/verify/otp")
