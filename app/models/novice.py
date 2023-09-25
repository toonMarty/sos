#!/usr/bin/env python3
"""
Define a Novice. A novice is a user who might experience a
problem while using software and requires the services of
an agent(IT technician)
"""
from app import db
from datetime import datetime


class Novice(db.Model):
    """
    Novice Definition
    """
    __tablename__ = 'novices'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    close_ticket = db.Column(db.Boolean, default=False)

    # user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    # tickets = db.relationship('Ticket', backref='novice', lazy='dynamic')

    # novice = db.relationship('User', foreign_keys=novice_id)

    def create_novice(self):
        """Persist a user object to a database"""
        db.session.add(self)
        db.session.commit()
