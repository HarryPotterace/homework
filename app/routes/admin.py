from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash

from app.decorators import admin_login_required
from app.extensions import db
from app.models import Admin, Appointment, AssessmentRecord, User, VentPost
from app.services.dashboard import build_dashboard_summary


admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


@admin_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"]
        admin = Admin.query.filter_by(username=username).first()
        if not admin or not check_password_hash(admin.password_hash, password):
            flash("后台账号或密码错误。", "danger")
            return redirect(url_for("admin.login"))

        session["admin_id"] = admin.id
        session["admin_name"] = admin.name
        session["admin_role"] = admin.role
        flash("后台登录成功。", "success")
        return redirect(url_for("admin.dashboard"))

    return render_template("admin/login.html")


@admin_bp.route("/logout")
def logout():
    session.pop("admin_id", None)
    session.pop("admin_name", None)
    session.pop("admin_role", None)
    flash("后台已退出。", "info")
    return redirect(url_for("admin.login"))


@admin_bp.route("/dashboard")
@admin_login_required
def dashboard():
    return render_template("admin/dashboard.html", summary=build_dashboard_summary())


@admin_bp.route("/assessments")
@admin_login_required
def assessments():
    records = (
        AssessmentRecord.query.join(User)
        .order_by(AssessmentRecord.created_at.desc())
        .all()
    )
    return render_template("admin/assessments.html", records=records)


@admin_bp.route("/vents")
@admin_login_required
def vents():
    posts = VentPost.query.order_by(VentPost.created_at.desc()).all()
    return render_template("admin/vents.html", posts=posts)


@admin_bp.route("/appointments", methods=["GET", "POST"])
@admin_login_required
def appointments():
    if request.method == "POST":
        appointment = Appointment.query.get_or_404(int(request.form["appointment_id"]))
        appointment.status = request.form["status"]
        db.session.commit()
        flash("预约状态已更新。", "success")
        return redirect(url_for("admin.appointments"))

    items = Appointment.query.order_by(Appointment.created_at.desc()).all()
    return render_template("admin/appointments.html", appointments=items)
