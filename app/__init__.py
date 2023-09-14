#!/usr/bin/env python3
"""
Setting up the application in a function
"""

from config import config
from flask import render_template, Flask
from flask_bootstrap import Bootstrap5
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from flask_moment import Moment
from elasticsearch import Elasticsearch
from flask_login import LoginManager


login_manager = LoginManager()
login_manager.login_view = 'auth.login'
bootstrap = Bootstrap5()
moment = Moment()


convention = {
  "ix": "ix_%(column_0_label)s",
  "uq": "uq_%(table_name)s_%(column_0_name)s",
  "ck": "ck_%(table_name)s_%(constraint_name)s",
  "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
  "pk": "pk_%(table_name)s"
}

db = SQLAlchemy(metadata=MetaData(naming_convention=convention))
migrate = Migrate()


def create_app(config_name):
    """
    Creating an app instance
    :param config_name: the name of the configuration to use
    :return: app instance
    """
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # set elasticsearch as an attribute because it lacks a flask extension wrapper
    app.elasticsearch = Elasticsearch([app.config['ELASTICSEARCH_URL']], request_timeout=60, verify_certs=False) \
        if app.config['ELASTICSEARCH_URL'] else None

    # Initialize the Flask application for use with the following
    # extension instances
    bootstrap.init_app(app)
    db.init_app(app)
    moment.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from app.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    with app.app_context():
        db.create_all()

    return app
