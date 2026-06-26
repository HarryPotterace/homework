from datetime import datetime, timedelta

from app import create_app, db
from app.models import (
    Appointment,
    AssessmentRecord,
    BehaviorLog,
    CounselorSchedule,
    User,
    VentPost,
)
from app.services.dashboard import build_dashboard_summary


def build_app():
    app = create_app(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        }
    )
    with app.app_context():
        db.create_all()
    return app


def test_admin_dashboard_requires_login():
    app = build_app()
    client = app.test_client()

    response = client.get("/admin/dashboard", follow_redirects=True)

    assert response.status_code == 200
    assert "\u54a8\u8be2\u5e08 / \u7ba1\u7406\u5458\u767b\u5f55".encode("utf-8") in response.data


def test_admin_can_login_and_view_dashboard():
    app = build_app()
    client = app.test_client()

    response = client.post(
        "/admin/login",
        data={
            "username": "admin",
            "password": "Admin12345",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert "\u5fc3\u7406\u4e2d\u5fc3\u540e\u53f0".encode("utf-8") in response.data


def test_admin_dashboard_exposes_workbench_sections():
    app = build_app()
    client = app.test_client()

    login_response = client.post(
        "/admin/login",
        data={
            "username": "admin",
            "password": "Admin12345",
        },
        follow_redirects=True,
    )
    assert login_response.status_code == 200

    response = client.get("/admin/dashboard")

    assert response.status_code == 200
    assert 'data-page="admin-dashboard"'.encode("utf-8") in response.data
    assert "\u5f85\u786e\u8ba4\u9884\u7ea6".encode("utf-8") in response.data
    assert "\u9700\u5173\u6ce8\u6811\u6d1e".encode("utf-8") in response.data


def test_admin_dashboard_includes_workbench_queues():
    app = build_app()
    client = app.test_client()

    login_response = client.post(
        "/admin/login",
        data={
            "username": "admin",
            "password": "Admin12345",
        },
        follow_redirects=True,
    )
    assert login_response.status_code == 200

    response = client.get("/admin/dashboard")

    assert response.status_code == 200
    assert 'id="admin-workbench"'.encode("utf-8") in response.data
    assert "\u5f85\u5904\u7406\u9884\u7ea6".encode("utf-8") in response.data
    assert "\u8fd1\u671f\u5f02\u5e38\u60c5\u7eea\u8bb0\u5f55".encode("utf-8") in response.data


def test_admin_dashboard_pending_queue_shows_only_pending_appointments():
    app = build_app()

    with app.app_context():
        pending_user = User(
            student_no="20260002",
            name="\u5f85\u5904\u7406\u5b66\u751f",
            nickname="\u6392\u961f\u6d4b\u8bd5",
            contact="pending@example.com",
            password_hash="hashed",
        )
        confirmed_user = User(
            student_no="20260003",
            name="\u5df2\u786e\u8ba4\u5b66\u751f",
            nickname="\u8fc7\u6ee4\u6d4b\u8bd5",
            contact="confirmed@example.com",
            password_hash="hashed",
        )
        db.session.add_all([pending_user, confirmed_user])
        db.session.flush()

        schedule = CounselorSchedule.query.first()
        now = datetime(2026, 6, 26, 15, 0, 0)

        db.session.add_all(
                [
                    Appointment(
                    user_id=pending_user.id,
                    schedule_id=schedule.id,
                    status="\u5f85\u786e\u8ba4",
                    note="\u5f85\u5904\u7406",
                    created_at=now,
                ),
                Appointment(
                    user_id=confirmed_user.id,
                    schedule_id=schedule.id,
                    status="\u5df2\u786e\u8ba4",
                    note="\u4e0d\u5e94\u51fa\u73b0",
                    created_at=now - timedelta(minutes=30),
                ),
            ]
        )
        db.session.commit()

    client = app.test_client()
    login_response = client.post(
        "/admin/login",
        data={
            "username": "admin",
            "password": "Admin12345",
        },
        follow_redirects=True,
    )
    assert login_response.status_code == 200

    response = client.get("/admin/dashboard")

    assert response.status_code == 200
    assert "\u5f85\u5904\u7406\u5b66\u751f".encode("utf-8") in response.data
    assert "\u5df2\u786e\u8ba4\u5b66\u751f".encode("utf-8") not in response.data


def test_admin_dashboard_includes_chart_hooks():
    app = build_app()
    client = app.test_client()

    login_response = client.post(
        "/admin/login",
        data={
            "username": "admin",
            "password": "Admin12345",
        },
        follow_redirects=True,
    )
    assert login_response.status_code == 200

    response = client.get("/admin/dashboard")

    assert response.status_code == 200
    assert 'id="emotion-distribution-chart"'.encode("utf-8") in response.data
    assert 'id="scale-usage-chart"'.encode("utf-8") in response.data
    assert 'data-dashboard-series='.encode("utf-8") in response.data
    assert 'src="/static/js/dashboard.js"'.encode("utf-8") in response.data


def test_admin_dashboard_focus_panel_uses_neutral_aggregate_wording():
    app = build_app()
    client = app.test_client()

    login_response = client.post(
        "/admin/login",
        data={
            "username": "admin",
            "password": "Admin12345",
        },
        follow_redirects=True,
    )
    assert login_response.status_code == 200

    response = client.get("/admin/dashboard")

    assert response.status_code == 200
    assert "\u5f53\u524d\u9700\u5173\u6ce8\u603b\u91cf".encode("utf-8") in response.data
    assert "\u6d4b\u8bc4\u7d2f\u8ba1\u603b\u91cf".encode("utf-8") in response.data
    assert "\u9884\u7ea6\u7d2f\u8ba1\u603b\u91cf".encode("utf-8") in response.data
    assert "\u6811\u6d1e\u7d2f\u8ba1\u6d3b\u8dc3".encode("utf-8") in response.data


def test_screen_page_shows_aggregated_metrics():
    app = build_app()
    client = app.test_client()

    response = client.get("/screen")

    assert response.status_code == 200
    assert "\u5b66\u9662\u5fc3\u7406\u6001\u52bf\u8131\u654f\u6570\u636e\u770b\u677f".encode("utf-8") in response.data


def test_screen_page_exposes_kpi_and_focus_panels():
    app = build_app()
    client = app.test_client()

    response = client.get("/screen")

    assert response.status_code == 200
    assert 'data-page="screen-dashboard"'.encode("utf-8") in response.data
    assert "\u5f53\u524d\u9700\u5173\u6ce8\u4eba\u6570".encode("utf-8") in response.data
    assert "\u4ec5\u5c55\u793a\u8131\u654f\u540e\u7684\u6c47\u603b\u6570\u636e".encode("utf-8") in response.data


def test_screen_page_includes_focus_kpis_and_timestamp():
    app = build_app()
    client = app.test_client()

    response = client.get("/screen")

    assert response.status_code == 200
    assert 'id="screen-kpis"'.encode("utf-8") in response.data
    assert "\u672c\u5468\u6d4b\u8bc4\u4eba\u6570".encode("utf-8") in response.data
    assert "\u9875\u9762\u5237\u65b0\u65f6\u95f4".encode("utf-8") in response.data


def test_screen_page_includes_focus_and_chart_sections():
    app = build_app()
    client = app.test_client()

    response = client.get("/screen")

    assert response.status_code == 200
    assert 'id="screen-focus-panel"'.encode("utf-8") in response.data
    assert 'id="screen-emotion-chart"'.encode("utf-8") in response.data
    assert 'id="screen-appointment-chart"'.encode("utf-8") in response.data
    assert 'id="screen-scale-chart"'.encode("utf-8") in response.data
    assert 'src="/static/js/screen.js"'.encode("utf-8") in response.data
    assert "\u4ec5\u5c55\u793a\u8131\u654f\u540e\u7684\u6c47\u603b\u6570\u636e".encode("utf-8") in response.data


def test_dashboard_summary_exposes_workbench_and_screen_focus_fields():
    app = build_app()

    with app.app_context():
        user = User(
            student_no="20260001",
            name="\u6d4b\u8bd5\u5b66\u751f",
            nickname="\u5c0f\u6d4b",
            contact="student@example.com",
            password_hash="hashed",
        )
        db.session.add(user)
        db.session.flush()

        schedule = CounselorSchedule.query.first()
        now = datetime(2026, 6, 26, 12, 0, 0)

        assessment = AssessmentRecord(
            user_id=user.id,
            scale_code="PHQ-9",
            scale_name="PHQ-9",
            score=14,
            result_level="\u4e2d\u5ea6",
            advice="\u5efa\u8bae\u6301\u7eed\u5173\u6ce8",
            created_at=now,
        )
        attention_post = VentPost(
            user_id=user.id,
            title="\u9700\u8981\u5e2e\u52a9",
            content="\u6700\u8fd1\u72b6\u6001\u4e0d\u592a\u597d",
            emotion="\u9700\u5173\u6ce8",
            risk_level="\u4e2d",
            is_anonymous=True,
            created_at=now,
        )
        regular_post = VentPost(
            user_id=user.id,
            title="\u666e\u901a\u53cd\u9988",
            content="\u4eca\u5929\u8fd8\u884c",
            emotion="\u5e73\u9759",
            risk_level="\u4f4e",
            is_anonymous=True,
            created_at=now - timedelta(hours=1),
        )
        behavior_log = BehaviorLog(
            user_id=user.id,
            page_name="home",
            mouse_speed=1.2,
            click_count=3,
            pause_count=1,
            emotion="\u9700\u5173\u6ce8",
            ui_mode="light",
            created_at=now,
        )
        pending_appointment = Appointment(
            user_id=user.id,
            schedule_id=schedule.id,
            status="\u5f85\u786e\u8ba4",
            note="\u9996\u6b21\u54a8\u8be2",
            created_at=now,
        )
        confirmed_appointment = Appointment(
            user_id=user.id,
            schedule_id=schedule.id,
            status="\u5df2\u786e\u8ba4",
            note="\u540e\u7eed\u56de\u8bbf",
            created_at=now - timedelta(hours=2),
        )

        db.session.add_all(
            [
                assessment,
                attention_post,
                regular_post,
                behavior_log,
                pending_appointment,
                confirmed_appointment,
            ]
        )
        db.session.commit()

        summary = build_dashboard_summary()

        assert summary["workbench"]["pending_appointments"] == 1
        assert summary["workbench"]["attention_posts"] == 1
        assert len(summary["workbench"]["recent_assessments"]) == 1
        assert len(summary["workbench"]["recent_attention_posts"]) == 1
        assert summary["workbench"]["recent_attention_posts"][0]["title"] == "\u9700\u8981\u5e2e\u52a9"
        assert len(summary["workbench"]["recent_appointments"]) == 2
        assert summary["screen_focus"]["attention_total"] == summary["emotion_counts"]["\u9700\u5173\u6ce8"] == 2
        assert summary["screen_focus"]["weekly_assessments"] == summary["kpis"]["assessments"] == 1
        assert summary["screen_focus"]["weekly_appointments"] == summary["kpis"]["appointments"] == 2
        assert summary["screen_focus"]["vent_activity"] == summary["kpis"]["posts"] == 2
