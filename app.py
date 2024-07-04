"""Initialize Flask app."""
from datetime import timedelta
from flask import Flask, session
from extensions import db, migrate, cors, api, ma, login_manager, jwt
from flask_jwt_extended.exceptions import NoAuthorizationError, WrongTokenError
import urls
from flask import jsonify, request
from user.models import User
import requests


PERMANENT_SESSION_LIFETIME = timedelta(hours=12)


def create_app(config_object="settings"):
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object(config_object)

    with app.app_context():
        register_extensions(app)
        register_blueprints(app)

        @app.before_request
        def make_session_permanent():
            session.permanent = True
            app.permanent_session_lifetime = PERMANENT_SESSION_LIFETIME

    return app


def register_extensions(app):
    """Register Flask extensions."""

    db.init_app(app)
    migrate.init_app(app, db)
    api.init_app(app)
    ma.init_app(app)
    cors.init_app(app, supports_credentials=True, resources={r"/api/*": {"origins": "*"}})
    login_manager.init_app(app)
    jwt.init_app(app)


def register_blueprints(app):
    """Register Flask blueprints."""
    app.register_blueprint(urls.blueprint, url_prefix="/api")
