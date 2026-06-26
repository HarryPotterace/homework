from app.models import Appointment, AssessmentRecord


def build_student_home_summary(user_id):
    latest_assessment = (
        AssessmentRecord.query.filter_by(user_id=user_id)
        .order_by(AssessmentRecord.created_at.desc())
        .first()
    )
    latest_appointment = (
        Appointment.query.filter_by(user_id=user_id)
        .order_by(Appointment.created_at.desc())
        .first()
    )

    if latest_assessment:
        recommended_action = "继续查看测评建议"
    elif latest_appointment:
        recommended_action = "查看预约进度"
    else:
        recommended_action = "先完成一次快速测评"

    return {
        "latest_assessment": latest_assessment,
        "latest_appointment": latest_appointment,
        "recommended_action": recommended_action,
    }
