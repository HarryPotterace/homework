from app import create_app, db


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
