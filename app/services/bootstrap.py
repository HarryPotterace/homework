from werkzeug.security import generate_password_hash

from app.data import SCALE_LIBRARY
from app.extensions import db
from app.models import Admin, CounselorSchedule, Scale, ScaleQuestion


def seed_reference_data():
    if Admin.query.count() == 0:
        db.session.add_all(
            [
                Admin(
                    username="consultant",
                    name="陈老师",
                    role="consultant",
                    contact="chen@example.com",
                    password_hash=generate_password_hash("Admin12345"),
                ),
                Admin(
                    username="admin",
                    name="系统管理员",
                    role="admin",
                    contact="admin@example.com",
                    password_hash=generate_password_hash("Admin12345"),
                ),
            ]
        )

    for code, detail in SCALE_LIBRARY.items():
        if not Scale.query.filter_by(code=code).first():
            db.session.add(
                Scale(
                    code=code,
                    name=detail["name"],
                    description=detail["description"],
                )
            )
        if ScaleQuestion.query.filter_by(scale_code=code).count() == 0:
            for index, question in enumerate(detail["questions"], start=1):
                db.session.add(
                    ScaleQuestion(
                        scale_code=code,
                        question_order=index,
                        content=question,
                    )
                )

    if CounselorSchedule.query.count() == 0:
        db.session.add_all(
            [
                CounselorSchedule(
                    counselor_name="陈老师",
                    title="国家二级心理咨询师",
                    schedule_date="2026-07-01",
                    slot="09:00-10:00",
                    is_available=True,
                ),
                CounselorSchedule(
                    counselor_name="李老师",
                    title="高校心理中心咨询师",
                    schedule_date="2026-07-01",
                    slot="15:00-16:00",
                    is_available=True,
                ),
                CounselorSchedule(
                    counselor_name="王老师",
                    title="学院专职辅导员",
                    schedule_date="2026-07-02",
                    slot="10:00-11:00",
                    is_available=True,
                ),
            ]
        )

    db.session.commit()
