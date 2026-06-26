from app import create_app, db


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
    assert "咨询师 / 管理员登录".encode("utf-8") in response.data


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
    assert "心理中心后台".encode("utf-8") in response.data


def test_screen_page_shows_aggregated_metrics():
    app = build_app()
    client = app.test_client()

    response = client.get("/screen")

    assert response.status_code == 200
    assert "学院心理态势脱敏数据看板".encode("utf-8") in response.data
