#!/usr/bin/env python3
"""
Error page rendering across the
application
"""
from flask import render_template
from . import main


@main.app_errorhandler(404)
def page_not_found(e):
    """Render if page not found"""
    return render_template('404.html'), 404


@main.app_errorhandler(500)
def internal_server_error(e):
    """Render internal server error"""
    return render_template('500.html'), 500
