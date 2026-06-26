from functools import wraps

from flask import flash, redirect, session, url_for


def student_login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get("user_id"):
            flash("请先登录学生账号。", "warning")
            return redirect(url_for("student.login"))
        return view(*args, **kwargs)

    return wrapped


def admin_login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get("admin_id"):
            flash("请先登录后台账号。", "warning")
            return redirect(url_for("admin.login"))
        return view(*args, **kwargs)

    return wrapped
