from app.data import SCALE_LIBRARY


def get_scale_catalog():
    return [
        {
            "code": code,
            "name": item["name"],
            "description": item["description"],
            "question_count": len(item["questions"]),
        }
        for code, item in SCALE_LIBRARY.items()
    ]


def get_scale_detail(scale_code):
    return SCALE_LIBRARY[scale_code]


def score_assessment(scale_code, answers):
    score = sum(int(answer) for answer in answers)

    if scale_code == "PHQ-9":
        if score <= 4:
            level = "无明显抑郁倾向"
            advice = "建议保持规律作息，并继续关注自己的情绪变化。"
        elif score <= 9:
            level = "轻度抑郁倾向"
            advice = "建议主动与朋友、辅导员或心理委员交流，并保持基本运动。"
        elif score <= 14:
            level = "中度抑郁倾向"
            advice = "建议尽快预约心理咨询，并减少高压任务堆积。"
        else:
            level = "重度抑郁倾向"
            advice = "建议立即联系心理中心或可信赖的老师，尽快获得专业支持。"
    else:
        if score <= 4:
            level = "无明显焦虑倾向"
            advice = "建议保持现有节奏，并留意近期压力源变化。"
        elif score <= 9:
            level = "轻度焦虑倾向"
            advice = "建议进行呼吸训练和规律休息，必要时预约咨询。"
        elif score <= 14:
            level = "中度焦虑倾向"
            advice = "建议尽快预约心理咨询，并适当降低近期压力负荷。"
        else:
            level = "重度焦虑倾向"
            advice = "建议立即联系心理中心，获得及时支持。"

    return {
        "score": score,
        "level": level,
        "advice": advice,
    }
