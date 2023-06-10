#!/usr/bin/env python3

""" Blueprint creation to define main routes"""
from flask import Blueprint

main = Blueprint('main', __name__)
print(__name__)
from . import views, errors
