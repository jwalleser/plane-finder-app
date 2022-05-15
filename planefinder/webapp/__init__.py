from flask import Flask
from planefinder.webapp import config


def create_app(config_name: str):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    from planefinder.webapp import db
    db.init_app(app)

    attach_routes_and_error_pages(app)

    return app

def attach_routes_and_error_pages(app: Flask):
    from planefinder.webapp import home
    app.register_blueprint(home.bp)
