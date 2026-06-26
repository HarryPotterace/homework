from datetime import datetime

from .extensions import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    student_no = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    nickname = db.Column(db.String(50), nullable=False)
    contact = db.Column(db.String(50), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)


class Admin(db.Model):
    __tablename__ = "admins"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    role = db.Column(db.String(20), nullable=False, default="consultant")
    contact = db.Column(db.String(50), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)


class Scale(db.Model):
    __tablename__ = "scales"

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)


class ScaleQuestion(db.Model):
    __tablename__ = "scale_questions"

    id = db.Column(db.Integer, primary_key=True)
    scale_code = db.Column(db.String(20), nullable=False)
    question_order = db.Column(db.Integer, nullable=False)
    content = db.Column(db.Text, nullable=False)


class AssessmentRecord(db.Model):
    __tablename__ = "assessment_records"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    scale_code = db.Column(db.String(20), nullable=False)
    scale_name = db.Column(db.String(100), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    result_level = db.Column(db.String(50), nullable=False)
    advice = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    user = db.relationship("User", backref="assessment_records")


class VentPost(db.Model):
    __tablename__ = "vent_posts"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    emotion = db.Column(db.String(20), nullable=False)
    risk_level = db.Column(db.String(20), nullable=False)
    is_anonymous = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    user = db.relationship("User", backref="vent_posts")


class BehaviorLog(db.Model):
    __tablename__ = "behavior_logs"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    page_name = db.Column(db.String(50), nullable=False)
    mouse_speed = db.Column(db.Float, nullable=False, default=0)
    click_count = db.Column(db.Integer, nullable=False, default=0)
    pause_count = db.Column(db.Integer, nullable=False, default=0)
    emotion = db.Column(db.String(20), nullable=False)
    ui_mode = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    user = db.relationship("User", backref="behavior_logs")


class CounselorSchedule(db.Model):
    __tablename__ = "counselors_schedule"

    id = db.Column(db.Integer, primary_key=True)
    counselor_name = db.Column(db.String(50), nullable=False)
    title = db.Column(db.String(50), nullable=False)
    schedule_date = db.Column(db.String(20), nullable=False)
    slot = db.Column(db.String(50), nullable=False)
    is_available = db.Column(db.Boolean, nullable=False, default=True)


class Appointment(db.Model):
    __tablename__ = "appointments"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    schedule_id = db.Column(db.Integer, db.ForeignKey("counselors_schedule.id"), nullable=False)
    status = db.Column(db.String(20), nullable=False, default="待确认")
    note = db.Column(db.String(255), nullable=False, default="")
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    user = db.relationship("User", backref="appointments")
    schedule = db.relationship("CounselorSchedule", backref="appointments")
