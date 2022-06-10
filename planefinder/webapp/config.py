import os
from collections.abc import MutableMapping
from planefinder.data import Database
import planefinder.data

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    # NOTE: Only uppercase class variables are put into the config dictionary!
    SECRET_KEY = "hard to guess string"

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG: bool = True
    DB: planefinder.data.Database = Database.mongodb(planefinder.data.DEV_DATABASE_NAME)


class TestingConfig(Config):
    TESTING = True
    DB: planefinder.data.Database = Database.mongodb(planefinder.data.TEST_DATABASE_NAME)


class ProductionConfig(Config):
    DB: planefinder.data.Database = Database.mongodb(planefinder.data.PROD_DATABASE_NAME)


config: MutableMapping[str, type] = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
