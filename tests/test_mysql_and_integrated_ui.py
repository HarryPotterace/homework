import os

import pytest

from app import create_app


def build_test_app():
    return create_app(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        }
    )


def test_home_route_uses_optimized_student_homepage():
    app = build_test_app()
    client = app.test_client()

    response = client.get("/")

    assert response.status_code == 200
    assert "先做眼前最需要的一步".encode("utf-8") in response.data
    assert "行动优先支持入口".encode("utf-8") in response.data


def test_screen_route_uses_optimized_situation_board():
    app = build_test_app()
    client = app.test_client()

    response = client.get("/screen")

    assert response.status_code == 200
    assert "页面刷新时间".encode("utf-8") in response.data
    assert "值班关注焦点".encode("utf-8") in response.data


def test_create_app_requires_database_url_outside_testing(monkeypatch):
    monkeypatch.delenv("DATABASE_URL", raising=False)

    with pytest.raises(RuntimeError, match="DATABASE_URL"):
        create_app()


def test_create_app_rejects_non_mysql_database_url_outside_testing(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "sqlite:///mental_health_system.db")

    with pytest.raises(RuntimeError, match="MySQL"):
        create_app()


def test_create_app_accepts_explicit_testing_database():
    app = build_test_app()

    assert app.config["TESTING"] is True
    assert app.config["SQLALCHEMY_DATABASE_URI"] == "sqlite:///:memory:"
