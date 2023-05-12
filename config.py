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
    # Avoid incurring memory overhead by setting
    # SQLALCHEMY_TRACK_MODIFICATIONS to False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    """Define Development configuration"""
    DEBUG = True
    # The database URI that will be used for the connection
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DB_URL') or \
        'sqlite:///' + os.path.join(base_directory, 'sos-db-dev.sqlite')


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
