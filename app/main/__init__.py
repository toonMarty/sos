#!/usr/bin/env python3

""" Blueprint creation to define routes"""
from flask import Blueprint
from app.models.role import Permission

main = Blueprint('main', __name__)
print(__name__)
from . import views, errors


@main.app_context_processor
def inject_permissions():
    """
    Check permissions from templates
    """
    return dict(Permission=Permission)
