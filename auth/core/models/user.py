import bcrypt
import datetime
import hashlib
import random

from flask.ext.login import UserMixin

from auth import db, login_manager


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(128))
    superuser = db.Column(db.Boolean, default=False)

    registration_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    active = db.Column(db.Boolean, default=False)
    activation_key = db.Column(db.String(128))

    display_name = db.Column(db.String(64))

    @property
    def groups(self):
        from auth.groups.models import GroupMembership
        return [membership.group for membership in GroupMembership.query.filter_by(member_id=self.id, app_pending=False).all()]

    def __init__(self, username=None, email=None, password=None):
        if username:
            self.username = username
        if email:
            self.email = email
        if password:
            self.set_password(password)

        self.registration_date = datetime.datetime.utcnow()
        self.active = False

    def set_password(self, plaintext_password):
        self.password = bcrypt.hashpw(plaintext_password.encode('utf-8'), bcrypt.gensalt())

    def validate_password(self, plaintext_password):
        return bcrypt.hashpw(plaintext_password.encode('utf-8'), bytes(self.password.encode('utf-8'))) == bytes(self.password.encode('utf-8'))

    def activate(self):
        self.active = True
        self.activation_key = None
        return self.active

    def generate_activation_key(self):
        salt = hashlib.sha1(
            str(random.random()).encode('utf-8')
        ).hexdigest()[:10]

        encodable = self.username+salt+self.email
        encodable = encodable.encode('utf-8')

        self.activation_key = hashlib.sha1(encodable).hexdigest()
        return True

    def get_display_name(self):
        if self.display_name:
            return self.display_name
        else:
            return self.username

    def has_role(self, role):
        if self.superuser:
            return True
        elif role in self.get_roles():
            return True
        else:
            return False

    def get_roles(self):
        return []

    def in_group(self, group):
        from auth.groups.models import GroupMembership
        return bool(GroupMembership.query.filter_by(group_id=group.id, member_id=self.id, app_pending=False).first())

@login_manager.user_loader
def load_user(userid):
    return User.query.filter_by(id=userid, active=True).first()