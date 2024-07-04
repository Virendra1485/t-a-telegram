# -*- coding: utf-8 -*-
"""Extensions module. Each extension is initialized in the app factory located in app.py."""
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_restful import Api
from flask_marshmallow import Marshmallow
from flask_login import LoginManager

db = SQLAlchemy()
migrate = Migrate(compare_type=True)
cors = CORS()
api = Api()
ma = Marshmallow()
login_manager = LoginManager()
jwt = JWTManager()
