from sqlalchemy import func

from app.models import Appointment, AssessmentRecord, BehaviorLog, CounselorSchedule, User, VentPost


RECENT_ITEMS_LIMIT = 5
ATTENTION_EMOTION = "需关注"
PENDING_APPOINTMENT_STATUS = "待确认"


def _serialize_datetime(value):
    return value.isoformat() if value else None


def build_dashboard_summary():
    total_students = User.query.count()
    total_assessments = AssessmentRecord.query.count()
    total_posts = VentPost.query.count()
    total_appointments = Appointment.query.count()

    emotion_counts = {"平静": 0, "焦虑": 0, "低落": 0, ATTENTION_EMOTION: 0}
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

    pending_appointments = Appointment.query.filter_by(
        status=PENDING_APPOINTMENT_STATUS
    ).count()
    attention_posts = VentPost.query.filter_by(emotion=ATTENTION_EMOTION).count()

    recent_assessments = (
        AssessmentRecord.query.join(User)
        .with_entities(
            AssessmentRecord.id,
            User.name,
            AssessmentRecord.scale_name,
            AssessmentRecord.score,
            AssessmentRecord.result_level,
            AssessmentRecord.created_at,
        )
        .order_by(AssessmentRecord.created_at.desc(), AssessmentRecord.id.desc())
        .limit(RECENT_ITEMS_LIMIT)
        .all()
    )

    recent_attention_posts = (
        VentPost.query.with_entities(
            VentPost.id,
            VentPost.title,
            VentPost.emotion,
            VentPost.is_anonymous,
            VentPost.created_at,
        )
        .filter(VentPost.emotion == ATTENTION_EMOTION)
        .order_by(VentPost.created_at.desc(), VentPost.id.desc())
        .limit(RECENT_ITEMS_LIMIT)
        .all()
    )

    recent_appointments = (
        Appointment.query.join(User)
        .join(CounselorSchedule)
        .with_entities(
            Appointment.id,
            User.name,
            CounselorSchedule.counselor_name,
            CounselorSchedule.schedule_date,
            CounselorSchedule.slot,
            Appointment.status,
            Appointment.created_at,
        )
        .order_by(Appointment.created_at.desc(), Appointment.id.desc())
        .limit(RECENT_ITEMS_LIMIT)
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
        "workbench": {
            "pending_appointments": pending_appointments,
            "attention_posts": attention_posts,
            "recent_assessments": [
                {
                    "id": item.id,
                    "student_name": item.name,
                    "scale_name": item.scale_name,
                    "score": item.score,
                    "result_level": item.result_level,
                    "created_at": _serialize_datetime(item.created_at),
                }
                for item in recent_assessments
            ],
            "recent_attention_posts": [
                {
                    "id": item.id,
                    "title": item.title,
                    "emotion": item.emotion,
                    "is_anonymous": item.is_anonymous,
                    "created_at": _serialize_datetime(item.created_at),
                }
                for item in recent_attention_posts
            ],
            "recent_appointments": [
                {
                    "id": item.id,
                    "student_name": item.name,
                    "counselor_name": item.counselor_name,
                    "schedule_date": item.schedule_date,
                    "slot": item.slot,
                    "status": item.status,
                    "created_at": _serialize_datetime(item.created_at),
                }
                for item in recent_appointments
            ],
        },
        "screen_focus": {
            "attention_total": emotion_counts.get(ATTENTION_EMOTION, 0),
            "weekly_assessments": total_assessments,
            "weekly_appointments": total_appointments,
            "vent_activity": total_posts,
        },
    }
