from planefinder.webapp import db
from flask import render_template, Blueprint

bp = Blueprint("home", __name__, url_prefix="/")

@bp.route("/")
def home():
    return render_template(
        "index.html", listings=db.get_db().get_all_listings()
    )
