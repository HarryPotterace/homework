HIGH_RISK_KEYWORDS = ["撑不下去", "不想活", "伤害自己", "消失", "绝望"]
LOW_MOOD_KEYWORDS = ["难受", "低落", "没力气", "不想说话", "睡不着"]
ANXIOUS_KEYWORDS = ["紧张", "焦虑", "慌", "压力", "害怕"]


def infer_text_emotion(content):
    text = content.strip()
    risk_hits = sum(1 for word in HIGH_RISK_KEYWORDS if word in text)
    low_hits = sum(1 for word in LOW_MOOD_KEYWORDS if word in text)
    anxious_hits = sum(1 for word in ANXIOUS_KEYWORDS if word in text)

    if risk_hits >= 1 or (low_hits >= 2 and "撑不下去" in text):
        return {"emotion": "需关注", "risk_level": "high"}
    if anxious_hits >= 2:
        return {"emotion": "焦虑", "risk_level": "medium"}
    if low_hits >= 1:
        return {"emotion": "低落", "risk_level": "medium"}
    return {"emotion": "平静", "risk_level": "low"}


def infer_behavior_emotion(metrics):
    mouse_speed = float(metrics.get("mouse_speed", 0))
    click_count = int(metrics.get("click_count", 0))
    pause_count = int(metrics.get("pause_count", 0))

    if mouse_speed >= 7 or click_count >= 10:
        return {"emotion": "焦虑", "ui_mode": "calm-down"}
    if pause_count >= 7:
        return {"emotion": "低落", "ui_mode": "gentle"}
    return {"emotion": "平静", "ui_mode": "default"}
