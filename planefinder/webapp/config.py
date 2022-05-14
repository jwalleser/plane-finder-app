import os
from planefinder.data import Database
import planefinder.data

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = "hard to guess string"

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    db = Database.mongodb(planefinder.data.DEV_DATABASE_NAME)


class TestingConfig(Config):
    TESTING = True
    db = Database.mongodb(planefinder.data.TEST_DATABASE_NAME)


class ProductionConfig(Config):
    db = Database.mongodb(planefinder.data.PROD_DATABASE_NAME)


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
