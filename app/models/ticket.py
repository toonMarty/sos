#!/usr/bin/env python3
"""
Ticket Model.
"""
from sqlalchemy import text, func

from app import db

from datetime import datetime
from .searchable_mixin import SearchableMixin
import random


class Ticket(SearchableMixin, db.Model):
    """Define tickets."""
    __searchable__ = ['subject', 'issue_description']
    __tablename__ = 'tickets'

    id = db.Column(db.Integer, primary_key=True)
    ticket_owner = db.Column(db.String(64), nullable=False)
    subject = db.Column(db.String(64), nullable=False)
    issue_description = db.Column(db.Text, nullable=False)
    date_submitted = db.Column(db.DateTime(), default=datetime.utcnow)
    ticket_priority = db.Column(db.String(20))

    team_viewer_id = db.Column(db.String(255), default='000')
    team_viewer_session_password = db.Column(db.String(255), nullable=False)

    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'))


    def create_ticket(self):
        """
        Persist ticket instances to database
        """
        db.session.add(self)
        db.session.commit()

    def get_ticket_subject_first_letter(self):
        """
        Get the first letter of the subject of a ticket object.
        For instance if the ticket subject is AVPro, the method will
        return the character 'A'.
        :return: the first character of a ticket object
        """
        return self.subject[0].upper()

    def get_ticket_submitted_time(self):
        """
        get the date the ticket was submitted in the format
        of hours, minutes and seconds
        """
        return self.date_submitted.time()

    def ticket_count(self):
        """
        Total ticket count for a particular user
        """
        return db.session.query(Ticket.id).count()
