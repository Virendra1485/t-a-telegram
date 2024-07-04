from extensions import db
from datetime import datetime


class BaseModel(db.Model):
    """
    An abstract base model that provides self-updating
    ``created_at`` and ``updated_at`` fields.
    """

    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime)
    deleted_at = db.Column(db.DateTime)
