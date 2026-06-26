from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from app.decorators import student_login_required
from app.extensions import db
from app.models import Appointment, AssessmentRecord, CounselorSchedule, User, VentPost
from app.services.assessment import get_scale_catalog, get_scale_detail, score_assessment
from app.services.emotion import infer_text_emotion


student_bp = Blueprint("student", __name__)


@student_bp.route("/")
def home():
    return render_template("student/home.html", scales=get_scale_catalog())


@student_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        student_no = request.form["student_no"].strip()
        if User.query.filter_by(student_no=student_no).first():
            flash("该学号已注册。", "danger")
            return redirect(url_for("student.register"))

        user = User(
            student_no=student_no,
            name=request.form["name"].strip(),
            nickname=request.form["nickname"].strip(),
            contact=request.form["contact"].strip(),
            password_hash=generate_password_hash(request.form["password"]),
        )
        db.session.add(user)
        db.session.commit()
        flash("注册成功，请登录。", "success")
        return redirect(url_for("student.login"))

    return render_template("student/register.html")


@student_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        student_no = request.form["student_no"].strip()
        password = request.form["password"]
        user = User.query.filter_by(student_no=student_no).first()

        if not user or not check_password_hash(user.password_hash, password):
            flash("学号或密码错误。", "danger")
            return redirect(url_for("student.login"))

        session.clear()
        session["user_id"] = user.id
        session["user_name"] = user.nickname
        flash("欢迎回来，你已成功登录。", "success")
        return redirect(url_for("student.home"))

    return render_template("student/login.html")


@student_bp.route("/logout")
def logout():
    session.clear()
    flash("你已退出登录。", "info")
    return redirect(url_for("student.home"))


@student_bp.route("/profile", methods=["GET", "POST"])
@student_login_required
def profile():
    user = User.query.get_or_404(session["user_id"])
    if request.method == "POST":
        user.nickname = request.form["nickname"].strip()
        user.contact = request.form["contact"].strip()
        db.session.commit()
        session["user_name"] = user.nickname
        flash("个人信息已更新。", "success")
        return redirect(url_for("student.profile"))

    return render_template("student/profile.html", user=user)


@student_bp.route("/assessment", methods=["GET", "POST"])
@student_login_required
def assessment():
    scale_code = request.args.get("scale", "PHQ-9")
    scale = get_scale_detail(scale_code)
    result = None

    if request.method == "POST":
        scale_code = request.form["scale_code"]
        scale = get_scale_detail(scale_code)
        answers = [request.form[f"q{index}"] for index in range(1, len(scale["questions"]) + 1)]
        result = score_assessment(scale_code, answers)
        record = AssessmentRecord(
            user_id=session["user_id"],
            scale_code=scale_code,
            scale_name=scale["name"],
            score=result["score"],
            result_level=result["level"],
            advice=result["advice"],
        )
        db.session.add(record)
        db.session.commit()
        flash("测评结果已保存。", "success")

    return render_template(
        "student/assessment.html",
        scales=get_scale_catalog(),
        active_scale=scale_code,
        scale=scale,
        result=result,
    )


@student_bp.route("/vent", methods=["GET", "POST"])
@student_login_required
def vent():
    posts = VentPost.query.order_by(VentPost.created_at.desc()).limit(6).all()
    result = None
    if request.method == "POST":
        title = request.form["title"].strip()
        content = request.form["content"].strip()
        result = infer_text_emotion(content)
        post = VentPost(
            user_id=session["user_id"],
            title=title,
            content=content,
            emotion=result["emotion"],
            risk_level=result["risk_level"],
            is_anonymous=True,
        )
        db.session.add(post)
        db.session.commit()
        flash("树洞内容已匿名保存。", "success")
        posts = VentPost.query.order_by(VentPost.created_at.desc()).limit(6).all()

    return render_template("student/vent.html", posts=posts, result=result)


@student_bp.route("/emotion")
@student_login_required
def emotion():
    return render_template("student/emotion.html")


@student_bp.route("/appointments", methods=["GET", "POST"])
@student_login_required
def appointments():
    if request.method == "POST":
        schedule = CounselorSchedule.query.get_or_404(int(request.form["schedule_id"]))
        if not schedule.is_available:
            flash("该时段已被预约，请重新选择。", "danger")
            return redirect(url_for("student.appointments"))

        appointment = Appointment(
            user_id=session["user_id"],
            schedule_id=schedule.id,
            note=request.form.get("note", "").strip(),
            status="待确认",
        )
        schedule.is_available = False
        db.session.add(appointment)
        db.session.commit()
        flash("预约申请已提交。", "success")
        return redirect(url_for("student.appointments"))

    schedules = CounselorSchedule.query.order_by(CounselorSchedule.schedule_date.asc()).all()
    my_items = (
        Appointment.query.filter_by(user_id=session["user_id"])
        .order_by(Appointment.created_at.desc())
        .all()
    )
    return render_template("student/appointments.html", schedules=schedules, appointments=my_items)


@student_bp.route("/appointments/<int:appointment_id>/cancel", methods=["POST"])
@student_login_required
def cancel_appointment(appointment_id):
    appointment = Appointment.query.get_or_404(appointment_id)
    if appointment.user_id != session["user_id"]:
        flash("你无权取消该预约。", "danger")
        return redirect(url_for("student.appointments"))

    appointment.status = "已取消"
    appointment.schedule.is_available = True
    db.session.commit()
    flash("预约已取消。", "info")
    return redirect(url_for("student.appointments"))
