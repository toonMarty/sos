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
    novice_name = db.Column(db.String(128), nullable=False)
    novice_username = db.Column(db.String(64), unique=True, nullable=False)
    novice_department = db.Column(db.String(32), nullable=False)
    created_on = db.Column(db.DateTime(), default=datetime.now)
    updated_on = db.Column(db.DateTime(), default=datetime.now, onupdate=datetime.now)

    tickets = db.relationship('Ticket', backref='novice', lazy='dynamic')

    def create_novice(self):
        """Persist a user object to a database"""
        db.session.add(self)
        db.session.commit()
