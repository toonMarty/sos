#!/usr/bin/env python3

"""
Define a user. A user is anyone who
uses the sos system. For this iterationn
the users include:
- Novice
- Agent
"""
from app import db, login_manager
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, LoginManager



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
