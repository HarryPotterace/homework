from pathlib import Path


def test_schema_sql_contains_required_tables():
    content = Path("sql/schema.sql").read_text(encoding="utf-8")

    for table_name in [
        "users",
        "admins",
        "scales",
        "scale_questions",
        "assessment_records",
        "vent_posts",
        "behavior_logs",
        "counselors_schedule",
        "appointments",
    ]:
        assert f"CREATE TABLE {table_name}" in content


def test_seed_sql_contains_core_seed_data():
    content = Path("sql/seed.sql").read_text(encoding="utf-8")

    assert "INSERT INTO admins" in content
    assert "INSERT INTO scales" in content
    assert "INSERT INTO counselors_schedule" in content
    assert "PHQ-9" in content
    assert "GAD-7" in content
