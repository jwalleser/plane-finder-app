from flask import g, current_app, Flask

from planefinder.data import Database

def get_db() -> Database:
    if "db" not in g:
        g.db = current_app.config["DB"]
    return g.db

def close_db(e=None) -> None:
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db() -> None:
    pass


def init_app(app: Flask) -> None:
    app.teardown_appcontext(close_db)