#!/usr/bin/env python3
"""
Setting up the application in a function
"""
from config import config
from flask import render_template, Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

bootstrap = Bootstrap()
db = SQLAlchemy()


def create_app(config_name):
    """
    Creating an app instance
    :param config_name: the name of the configuration to use
    :return: app instance
    """
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # Initialize the Flask application for use with the following
    # extension instances
    bootstrap.init_app(app)
    db.init_app(app)

    return app
