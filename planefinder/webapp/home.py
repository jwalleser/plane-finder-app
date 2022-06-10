from planefinder.webapp import db
from flask import render_template, Blueprint

bp = Blueprint("home", __name__, url_prefix="/")

@bp.route("/")
def home():
    db.get_db().get_all_listings()
    return render_template("index.html", listings=[])
