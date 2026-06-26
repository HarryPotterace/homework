from flask import Blueprint, jsonify, request, session

from app.extensions import db
from app.models import BehaviorLog
from app.services.dashboard import build_dashboard_summary
from app.services.emotion import infer_behavior_emotion


api_bp = Blueprint("api", __name__, url_prefix="/api")


@api_bp.route("/behavior", methods=["POST"])
def behavior():
    payload = request.get_json() or {}
    result = infer_behavior_emotion(payload)
    log = BehaviorLog(
        user_id=session.get("user_id"),
        page_name=payload.get("page_name", "unknown"),
        mouse_speed=float(payload.get("mouse_speed", 0)),
        click_count=int(payload.get("click_count", 0)),
        pause_count=int(payload.get("pause_count", 0)),
        emotion=result["emotion"],
        ui_mode=result["ui_mode"],
    )
    db.session.add(log)
    db.session.commit()
    return jsonify(result)


@api_bp.route("/screen-data")
def screen_data():
    return jsonify(build_dashboard_summary())
