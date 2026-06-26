from flask import Blueprint, render_template

from app.services.dashboard import build_dashboard_summary


screen_bp = Blueprint("screen", __name__)


@screen_bp.route("/screen")
def screen():
    return render_template("screen/index.html", summary=build_dashboard_summary())
