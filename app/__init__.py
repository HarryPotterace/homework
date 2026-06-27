from pathlib import Path
import os

from flask import Flask, session

from app.config import Config
from app.extensions import db
from app.routes.admin import admin_bp
from app.routes.api import api_bp
from app.routes.screen import screen_bp
from app.routes.student import student_bp
from app.services.bootstrap import seed_reference_data


def validate_database_uri(app):
    database_uri = app.config.get("SQLALCHEMY_DATABASE_URI")

    if app.config.get("TESTING"):
        if not database_uri:
            raise RuntimeError("Testing mode requires an explicit SQLALCHEMY_DATABASE_URI.")
        return

    if not database_uri:
        raise RuntimeError(
            "DATABASE_URL is required and must point to a MySQL database."
        )

    if not database_uri.startswith("mysql+pymysql://"):
        raise RuntimeError(
            "MySQL is required for runtime execution. Use a mysql+pymysql:// DATABASE_URL."
        )


def create_app(test_config=None):
    project_root = Path(__file__).resolve().parent.parent
    app = Flask(
        __name__,
        instance_relative_config=True,
        template_folder=str(project_root / "templates"),
        static_folder=str(project_root / "static"),
    )
    app.config.from_object(Config)

    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", app.config["SECRET_KEY"])
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")

    if test_config:
        app.config.update(test_config)

    validate_database_uri(app)
    db.init_app(app)
    app.register_blueprint(student_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(screen_bp)
    app.register_blueprint(api_bp)

    @app.context_processor
    def inject_session_data():
        return {
            "student_logged_in": bool(session.get("user_id")),
            "student_name": session.get("user_name"),
            "admin_logged_in": bool(session.get("admin_id")),
            "admin_name": session.get("admin_name"),
            "admin_role": session.get("admin_role"),
        }

    with app.app_context():
        db.create_all()
        seed_reference_data()

    return app
