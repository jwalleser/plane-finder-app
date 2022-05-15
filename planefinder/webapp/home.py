from flask import render_template, Blueprint

bp = Blueprint("home", __name__, url_prefix="/")

@bp.route("/")
def home():
    render_template("index.html")
