#!/usr/bin/env python3

"""
Agent definition. An agent solves a ticket
submitted by a novice
"""
from app import db


class Agent(db.Model):
    """
    Define an agent
    """
    __tablename__ = 'agents'

    agent_id = db.Column(db.Integer, primary_key=True)
    agent_name = db.Column(db.String(64), nullable=False)
