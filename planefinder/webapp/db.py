from flask import g, current_app, Flask

from planefinder.data import Database
from planefinder import logging


def get_db() -> Database:
    if "db" not in g:
        g.db = current_app.config["DB"]
    return g.db


def close_db(e=None) -> None:
    db = g.pop("db", None)
    log = logging.get_logger(__name__)
    log.debug(f"Closing db: {db}")

    if db is not None:
        # db.close()
        # TODO: I really do want to be able to
        # close the database, but this statement seems to break the app.
        pass


def init_db() -> None:
    pass


def init_app(app: Flask) -> None:
    app.teardown_appcontext(close_db)
