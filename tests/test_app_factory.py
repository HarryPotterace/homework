from app import create_app


def test_home_route_responds_successfully():
    app = create_app(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        }
    )
    client = app.test_client()

    response = client.get("/")

    assert response.status_code == 200
    assert "智慧校园心理辅导".encode("utf-8") in response.data
