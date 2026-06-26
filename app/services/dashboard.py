from sqlalchemy import func

from app.models import Appointment, AssessmentRecord, BehaviorLog, CounselorSchedule, User, VentPost


def build_dashboard_summary():
    total_students = User.query.count()
    total_assessments = AssessmentRecord.query.count()
    total_posts = VentPost.query.count()
    total_appointments = Appointment.query.count()

    emotion_counts = {"平静": 0, "焦虑": 0, "低落": 0, "需关注": 0}
    for emotion, count in (
        BehaviorLog.query.with_entities(BehaviorLog.emotion, func.count(BehaviorLog.id))
        .group_by(BehaviorLog.emotion)
        .all()
    ):
        emotion_counts[emotion] = count
    for emotion, count in (
        VentPost.query.with_entities(VentPost.emotion, func.count(VentPost.id))
        .group_by(VentPost.emotion)
        .all()
    ):
        emotion_counts[emotion] = emotion_counts.get(emotion, 0) + count

    scale_stats = {"PHQ-9": 0, "GAD-7": 0}
    for code, count in (
        AssessmentRecord.query.with_entities(
            AssessmentRecord.scale_code,
            func.count(AssessmentRecord.id),
        )
        .group_by(AssessmentRecord.scale_code)
        .all()
    ):
        scale_stats[code] = count

    schedule_hotspots = (
        Appointment.query.join(CounselorSchedule)
        .with_entities(CounselorSchedule.schedule_date, func.count(Appointment.id))
        .group_by(CounselorSchedule.schedule_date)
        .order_by(CounselorSchedule.schedule_date.asc())
        .all()
    )

    return {
        "kpis": {
            "students": total_students,
            "assessments": total_assessments,
            "posts": total_posts,
            "appointments": total_appointments,
        },
        "emotion_counts": emotion_counts,
        "scale_stats": scale_stats,
        "schedule_hotspots": [
            {"date": date, "count": count} for date, count in schedule_hotspots
        ],
    }
