from pathlib import Path
import re

from werkzeug.security import check_password_hash


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def read_project_file(relative_path):
    return (PROJECT_ROOT / relative_path).read_text(encoding="utf-8")


def test_models_avoid_deprecated_datetime_utcnow_defaults():
    content = read_project_file("app/models.py")

    assert "datetime.utcnow" not in content


def test_backend_code_avoids_legacy_query_get_apis():
    legacy_references = []

    for relative_path in (
        "app/routes/admin.py",
        "app/routes/student.py",
        "tests/test_student_routes.py",
    ):
        content = read_project_file(relative_path)
        if ".query.get(" in content:
            legacy_references.append(f"{relative_path}: .query.get(")
        if ".query.get_or_404(" in content:
            legacy_references.append(f"{relative_path}: .query.get_or_404(")

    assert not legacy_references, "\n".join(legacy_references)


def test_seed_sql_admin_hashes_support_demo_login():
    content = read_project_file("sql/seed.sql")

    assert "placeholder" not in content

    for username in ("consultant", "admin"):
        match = re.search(
            rf"^\('{username}',.*'([^']+)'\)\s*[,;]?$",
            content,
            re.MULTILINE,
        )

        assert match is not None, f"missing admin seed row for {username}"
        assert check_password_hash(match.group(1), "Admin12345")
