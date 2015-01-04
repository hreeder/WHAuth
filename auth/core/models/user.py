import datetime

from flask.ext.login import UserMixin

from auth import db


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(128))

    registration_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    active = db.Column(db.Boolean)
    activation_key = db.Column(db.String(128))

    display_name = db.Column(db.String(64))

    @staticmethod
    def generate_password(plaintext_password):
        return plaintext_password

    def get_display_name(self):
        if self.display_name:
            return self.display_name
        else:
            return self.username