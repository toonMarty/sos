#!/usr/bin/env python3

"""
Configuration sets
"""
import os

# The directory where the app resides
base_directory = os.path.abspath(os.path.dirname(__file__))


class Config:
    """
    Define App configuration and environments
    """

    ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL')
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.googlemail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', '587'))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', 1]
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    SECRET_KEY = os.environ.get('SECRET_KEY')
    # Avoid incurring memory overhead by setting
    # SQLALCHEMY_TRACK_MODIFICATIONS to False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SOS_MAIL_SUBJECT_PREFIX = '[sos]'
    SOS_MAIL_SENDER = os.environ.get('SOS_MAIL_SENDER')
    SOS_ADMIN = os.environ.get('SOS_ADMIN')
    TICKETS_PER_PAGE = 25

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    """Define Development configuration"""
    DEBUG = True
    # The database URI that will be used for the connection
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DB_URL') or \
        'sqlite:///' + os.path.join(base_directory, 'sos-dev-dbase.sqlite')


class ProductionConfig(Config):
    """Define Production Configuration"""
    SQLALCHEMY_DATABASE_URI = os.environ.get('PROD_DB_URL') or \
        'sqlite:///' + os.path.join(base_directory, 'sos-db-prod.sqlite')


class TestConfig(Config):
    """Define Testing Configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DB_URL') or 'sqlite://'


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestConfig,
    'default': DevelopmentConfig
}
