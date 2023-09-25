#!/usr/bin/env python3

"""
Define a user. A user is anyone who
uses the sos system. For this iterationn
the users include:
- Novice
- Agent
"""
from app import db, login_manager
from app.models.role import Role, Permission
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, LoginManager, AnonymousUserMixin
import jwt
from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


class User(UserMixin, db.Model):
    """
    user definition
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(128), nullable=False)
    last_name = db.Column(db.String(128))
    username = db.Column(db.String(128), unique=True, nullable=False)
    email = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    department = db.Column(db.String(64), nullable=False)
    created_on = db.Column(db.DateTime(), default=datetime.now)
    updated_on = db.Column(db.DateTime(), default=datetime.now, onupdate=datetime.now)
    confirmed = db.Column(db.Boolean, default=False)

    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    tickets = db.relationship('Ticket', backref='sender', lazy='dynamic')

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)

        if self.role is None:
            if self.email == current_app.config['SOS_ADMIN']:
                self.role = Role.query.filter_by(name='Administrator').first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()
    @property
    def password(self):
        """
        Make Passwords in plain text an inaccessible property/unreadable
        """
        raise AttributeError('Password is not a readable attribute')

    @password.setter
    def password(self, password: str):
        """
        Generate a password hash
        Args:
            password: password to check hash function for
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """
        verify if hash matches plain text password.
        Args:
            password: the password to check against the hash
        """
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration=3600):
        """
        Generate confirmation token for user account
        Args:
            expiration (int): the time the generated token will be valid
        Return:
            reset_token: encoded(base64) token
        """
        confirmation_token = jwt.encode({
            "confirm": self.id,
            "exp": datetime.now(tz=timezone.utc)
            + timedelta(seconds=expiration)
        }, current_app.config['SECRET_KEY'], algorithm='HS256')

        return confirmation_token

    def confirm(self, token):
        """
        Token verification - Checks whether
        generated token matches the logged-in user
        Args:
            token: token to confirm
        Return:
            True: if token is confirmed
                  else
            False: token is not confirmed
        """
        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'],
                              algorithms=['HS256'],
                              leeway=timedelta(seconds=10))
        except:
            return False

        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    def generate_reset_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'])
        return s.dumps({'reset': self.id}).decode('utf-8')

    @staticmethod
    def reset_password(token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False

        user = User.query.get(data.get('reset'))
        if user is None:
            return False
        user.password = new_password
        db.session.add(user)
        return True

    def generate_email_change_token(self, new_email, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'change_email': self.id, 'new_email': new_email}).decode('utf-8')

    def change_email(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        if data.get('change_email') != self.id:
            return False
        new_email = data.get('new_email')
        if new_email is None:
            return False
        if self.query.filter_by(email=new_email).first() is not None:
            return False
        self.email = new_email
        db.session.add(self)
        return True

    def can(self, perm):
        return self.role is not None and self.role.has_permission(perm)

    def is_administrator(self):
        return self.can(Permission.ADMIN)


class AnonymousUser(AnonymousUserMixin):
    """
    Read-only access to anonymous users
    """
    def can(self, permissions):
        """
        Check whether an anonymous user has
        certain permissions
        Return:
            False: (why?)anonymous users have Read-only access to the site
        """
        return False

    def is_admin(self):
        """
        Verify is an anonymous user is an admin
        Return:
            False
        """
        return False


login_manager.anonymous_user = AnonymousUser


@login_manager.user_loader
def load_user(user_id: str) -> User:
    """
    Load user from database given the user identifier
    Args:
        user_id (str): the user identifier passed as a string
    Return:
        user object if user is found else None
    """
    return User.query.get(int(user_id))
