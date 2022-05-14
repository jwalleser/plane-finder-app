from flask import Flask


def create_app(config_name: str):
    app = Flask(__name__)
