from app import create_app, db
from app.models import Appointment, AssessmentRecord, CounselorSchedule, VentPost


def build_app():
    app = create_app(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
            "WTF_CSRF_ENABLED": False,
        }
    )
    with app.app_context():
        db.create_all()
    return app


def register_student(client, student_no="20250001"):
    return client.post(
        "/register",
        data={
            "student_no": student_no,
            "name": "张三",
            "nickname": "树洞旅人",
            "contact": "13800000000",
            "password": "StrongPass123",
        },
        follow_redirects=True,
    )


def login_student(client, student_no="20250001"):
    return client.post(
        "/login",
        data={
            "student_no": student_no,
            "password": "StrongPass123",
        },
        follow_redirects=True,
    )


def test_student_can_register_and_login():
    app = build_app()
    client = app.test_client()

    register_response = register_student(client)

    assert register_response.status_code == 200
    assert "注册成功".encode("utf-8") in register_response.data

    login_response = login_student(client)

    assert login_response.status_code == 200
    assert "欢迎回来".encode("utf-8") in login_response.data


def test_register_page_includes_validation_script():
    app = build_app()
    client = app.test_client()

    response = client.get("/register")

    assert response.status_code == 200
    assert b"validation.js" in response.data


def test_logged_in_student_can_fetch_schedule_options():
    app = build_app()
    client = app.test_client()
    register_student(client)
    login_student(client)

    response = client.get("/api/schedules")

    assert response.status_code == 200
    payload = response.get_json()
    assert isinstance(payload, list)
    assert payload
    assert {"id", "counselor_name", "schedule_date", "slot", "is_available"} <= set(payload[0])


def test_appointments_page_exposes_schedule_api_endpoint():
    app = build_app()
    client = app.test_client()
    register_student(client)
    login_student(client)

    response = client.get("/appointments")

    assert response.status_code == 200
    assert b"data-schedule-api" in response.data


def test_assessment_submission_creates_record():
    app = build_app()
    client = app.test_client()
    register_student(client)
    login_student(client)

    response = client.post(
        "/assessment",
        data={
            "scale_code": "PHQ-9",
            "q1": "2",
            "q2": "2",
            "q3": "1",
            "q4": "1",
            "q5": "2",
            "q6": "0",
            "q7": "1",
            "q8": "1",
            "q9": "1",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert "测评结果已保存".encode("utf-8") in response.data
    with app.app_context():
        record = AssessmentRecord.query.one()
        assert record.scale_code == "PHQ-9"
        assert record.score == 11


def test_vent_post_generates_emotion_label():
    app = build_app()
    client = app.test_client()
    register_student(client)
    login_student(client)

    response = client.post(
        "/vent",
        data={
            "title": "最近状态不太好",
            "content": "最近很难受，睡不着，也不想和任何人说话，感觉撑不下去了。",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert "需关注".encode("utf-8") in response.data
    with app.app_context():
        post = VentPost.query.one()
        assert post.emotion == "需关注"
        assert post.risk_level == "high"


def test_student_can_create_and_cancel_appointment():
    app = build_app()
    client = app.test_client()
    register_student(client)
    login_student(client)

    with app.app_context():
        schedule = CounselorSchedule.query.filter_by(is_available=True).first()
        schedule_id = schedule.id

    create_response = client.post(
        "/appointments",
        data={
            "schedule_id": str(schedule_id),
            "note": "希望安排在下午前沟通。",
        },
        follow_redirects=True,
    )

    assert create_response.status_code == 200
    assert "预约申请已提交".encode("utf-8") in create_response.data

    with app.app_context():
        appointment = Appointment.query.one()
        appointment_id = appointment.id
        assert appointment.status == "待确认"
        assert appointment.schedule.is_available is False

    cancel_response = client.post(
        f"/appointments/{appointment_id}/cancel",
        follow_redirects=True,
    )

    assert cancel_response.status_code == 200
    assert "预约已取消".encode("utf-8") in cancel_response.data
    with app.app_context():
        appointment = Appointment.query.get(appointment_id)
        assert appointment.status == "已取消"
        assert appointment.schedule.is_available is True
