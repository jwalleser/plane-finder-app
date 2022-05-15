from flask import g, current_app, Flask

def get_db():
    if "db" not in g:
        g.db = current_app.config.db
    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    pass


def init_app(app: Flask):
    app.teardown_appcontext(close_db)