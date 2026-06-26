from app.services.assessment import score_assessment
from app.services.emotion import infer_behavior_emotion, infer_text_emotion


def test_score_assessment_returns_expected_level_and_advice():
    result = score_assessment("PHQ-9", [2, 2, 1, 1, 2, 0, 1, 1, 1])

    assert result["score"] == 11
    assert result["level"] == "中度抑郁倾向"
    assert "建议尽快预约心理咨询" in result["advice"]


def test_infer_text_emotion_marks_high_risk_content():
    result = infer_text_emotion("最近特别难受，睡不着，也不想和任何人说话，感觉撑不下去了。")

    assert result["emotion"] == "需关注"
    assert result["risk_level"] == "high"


def test_infer_behavior_emotion_uses_interaction_signals():
    result = infer_behavior_emotion(
        {
            "mouse_speed": 8.5,
            "click_count": 12,
            "pause_count": 6,
        }
    )

    assert result["emotion"] == "焦虑"
    assert result["ui_mode"] == "calm-down"
