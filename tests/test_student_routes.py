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


def test_student_can_register_and_login():
    app = build_app()
    client = app.test_client()

    register_response = client.post(
        "/register",
        data={
            "student_no": "20250001",
            "name": "张三",
            "nickname": "树洞旅人",
            "contact": "13800000000",
            "password": "StrongPass123",
        },
        follow_redirects=True,
    )

    assert register_response.status_code == 200
    assert "注册成功".encode("utf-8") in register_response.data

    login_response = client.post(
        "/login",
        data={
            "student_no": "20250001",
            "password": "StrongPass123",
        },
        follow_redirects=True,
    )

    assert login_response.status_code == 200
    assert "欢迎回来".encode("utf-8") in login_response.data
