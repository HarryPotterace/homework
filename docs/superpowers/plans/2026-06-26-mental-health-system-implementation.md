# 智慧校园心理辅导与情绪感知交互子系统 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 构建一个覆盖学生端、后台端和大屏端的智慧校园心理辅导与情绪感知交互系统，并同步交付完整文档与数据库脚本。

**Architecture:** 使用 Flask 单体应用承载三端页面与少量 AJAX 接口，业务逻辑按认证、测评、情绪、预约、统计拆分。以 MySQL 为正式数据存储，测试阶段允许使用 SQLite，报告和部署文档统一围绕这一实现展开。

**Tech Stack:** Flask, Jinja2, Bootstrap, JavaScript, MySQL, PyMySQL, pytest

---

## File Structure
- `app/`：Flask 应用、模型、服务、路由。
- `templates/student/`：学生端页面。
- `templates/admin/`：后台页面。
- `templates/screen/`：大屏页面。
- `static/css/`、`static/js/`：样式、表单校验、行为采集、异步交互。
- `tests/`：单元测试与流程测试。
- `sql/`：建表、初始化数据。
- `docs/`：设计说明、实施计划、部署说明、数据库说明、测试记录、报告草稿。

## Delivery Order
1. 先建立文档总控，锁定每份文档的边界和用途。
2. 再补齐需求缺口和目录结构。
3. 再完善学生端主流程。
4. 然后补齐后台和大屏。
5. 最后整理 SQL 与全部文档。

## Document Control Rule
- `docs/document-control.md` 是交付文档的唯一入口。
- 实现过程中若需求、字段、页面、测试结果发生变化，必须先更新对应文档，再更新总控文档状态。
- 不允许让多个文档同时各自定义同一个主题；必须明确主来源。

### Task 0: 建立文档总控机制

**Files:**
- Create: `docs/document-control.md`
- Modify: `docs/superpowers/specs/2026-06-26-mental-health-system-design.md`
- Modify: `docs/superpowers/plans/2026-06-26-mental-health-system-implementation.md`

- [ ] **Step 1: 写总控文档存在性测试**

```python
def test_document_control_exists():
    assert Path("docs/document-control.md").exists()


def test_document_control_lists_core_deliverables():
    content = Path("docs/document-control.md").read_text(encoding="utf-8")
    assert "deployment-guide.md" in content
    assert "database-design.md" in content
    assert "course-report-outline.md" in content
```

- [ ] **Step 2: 运行测试确认失败**

Run: `pytest tests -q`
Expected: 因缺少 `docs/document-control.md` 或未登记核心文档而失败。

- [ ] **Step 3: 编写总控文档**

```markdown
# 项目交付文档总控
## 作用
## 文档登记表
## 冲突预防规则
## 更新顺序
```

- [ ] **Step 4: 在设计说明和实施计划中写入总控规则**

```markdown
- `docs/document-control.md` 是唯一文档入口。
- 每份文档必须写清用途、内容、依赖和状态。
```

- [ ] **Step 5: 重新运行测试**

Run: `pytest tests -q`
Expected: 总控文档相关检查通过。

### Task 0.5: 锁定报告模板与要求审计

**Files:**
- Create: `docs/requirements-audit.md`
- Create: `docs/course-report-outline.md`
- Modify: `docs/superpowers/specs/2026-06-26-mental-health-system-design.md`

- [ ] **Step 1: 写报告与要求骨架存在性测试**

```python
def test_report_outline_exists():
    assert Path("docs/course-report-outline.md").exists()


def test_requirements_audit_exists():
    assert Path("docs/requirements-audit.md").exists()
```

- [ ] **Step 2: 运行测试确认失败**

Run: `pytest tests -q`
Expected: 因缺少报告提纲或要求审计文档而失败。

- [ ] **Step 3: 编写报告模板骨架**

```markdown
## 第一章 系统需求分析
## 第二章 可行性分析
## 第三章 概要设计
## 第四章 系统详细设计与实现
## 第五章 系统测试
## 第六章 总结与展望
```

- [ ] **Step 4: 编写要求审计文档**

```markdown
| 要求 | 当前状态 | 对应文档/实现 |
| --- | --- | --- |
| B/S 结构系统 | 已锁定 | 设计说明 |
```

- [ ] **Step 5: 重新运行测试**

Run: `pytest tests -q`
Expected: 报告模板与要求审计相关检查通过。

### Task 1: 需求缺口校正与目录整理

**Files:**
- Modify: `app/routes/student.py`
- Modify: `templates/student/register.html`
- Modify: `templates/student/login.html`
- Modify: `templates/student/appointments.html`
- Create: `static/js/validation.js`
- Create: `sql/schema.sql`
- Create: `sql/seed.sql`

- [ ] **Step 1: 写出缺口回归测试**

```python
def test_register_page_has_password_strength_hook():
    response = client.get("/register")
    assert b"validation.js" in response.data


def test_appointments_page_uses_async_schedule_loading():
    response = client.get("/appointments", follow_redirects=True)
    assert b"data-schedule-api" in response.data
```

- [ ] **Step 2: 运行测试确认失败**

Run: `pytest tests -q`
Expected: 至少出现注册页缺少校验脚本、预约页缺少异步时段标记或相关元素断言失败。

- [ ] **Step 3: 实现最小修复**

```python
@student_bp.route("/api/schedules")
@student_login_required
def schedule_options():
    items = CounselorSchedule.query.order_by(CounselorSchedule.schedule_date.asc()).all()
    return jsonify(
        [
            {
                "id": item.id,
                "counselor_name": item.counselor_name,
                "title": item.title,
                "schedule_date": item.schedule_date,
                "slot": item.slot,
                "is_available": item.is_available,
            }
            for item in items
        ]
    )
```

- [ ] **Step 4: 补前端校验与异步加载**

```javascript
registerForm.addEventListener("submit", (event) => {
  if (password.value.length < 8) {
    event.preventDefault();
    alert("密码至少 8 位，并包含字母与数字。");
  }
});
```

- [ ] **Step 5: 重新运行测试**

Run: `pytest tests -q`
Expected: 需求缺口相关测试通过，其余失败保留给后续任务处理。

### Task 2: 完成学生端主流程

**Files:**
- Modify: `app/routes/student.py`
- Modify: `app/services/assessment.py`
- Modify: `app/services/emotion.py`
- Modify: `templates/student/assessment.html`
- Modify: `templates/student/vent.html`
- Modify: `templates/student/emotion.html`
- Test: `tests/test_student_routes.py`
- Test: `tests/test_services.py`

- [ ] **Step 1: 为注册登录、测评、树洞、预约补充失败测试**

```python
def test_assessment_submission_creates_record(client, student_session):
    response = client.post("/assessment", data={...}, follow_redirects=True)
    assert "测评结果已保存".encode("utf-8") in response.data


def test_vent_post_generates_emotion_label(client, student_session):
    response = client.post("/vent", data={"title": "test", "content": "最近很难受，睡不着"}, follow_redirects=True)
    assert "低落".encode("utf-8") in response.data
```

- [ ] **Step 2: 运行学生端测试确认失败**

Run: `pytest tests/test_student_routes.py tests/test_services.py -q`
Expected: 新增断言失败，提示测评、树洞、预约或情绪判断行为尚未满足。

- [ ] **Step 3: 实现最小业务代码**

```python
result = score_assessment(scale_code, answers)
record = AssessmentRecord(
    user_id=session["user_id"],
    scale_code=scale_code,
    scale_name=scale["name"],
    score=result["score"],
    result_level=result["level"],
    advice=result["advice"],
)
db.session.add(record)
db.session.commit()
```

- [ ] **Step 4: 让情绪页可见切换反馈**

```javascript
card.dataset.uiMode = result.ui_mode;
setField("emotion", result.emotion);
setField("mode", result.ui_mode);
```

- [ ] **Step 5: 重新运行学生端测试**

Run: `pytest tests/test_student_routes.py tests/test_services.py -q`
Expected: 学生主流程相关测试全部通过。

### Task 3: 完成后台与大屏

**Files:**
- Modify: `app/routes/admin.py`
- Modify: `app/routes/screen.py`
- Modify: `app/routes/api.py`
- Modify: `app/services/dashboard.py`
- Modify: `templates/admin/*.html`
- Modify: `templates/screen/index.html`
- Create: `tests/test_admin_and_screen.py`

- [ ] **Step 1: 写后台和大屏失败测试**

```python
def test_admin_dashboard_requires_login(client):
    response = client.get("/admin/dashboard", follow_redirects=True)
    assert "后台登录".encode("utf-8") in response.data


def test_screen_page_shows_aggregated_metrics(client):
    response = client.get("/screen")
    assert "学院心理态势脱敏数据看板".encode("utf-8") in response.data
```

- [ ] **Step 2: 运行测试确认失败**

Run: `pytest tests/test_admin_and_screen.py -q`
Expected: 至少有后台鉴权、统计字段或大屏内容断言失败。

- [ ] **Step 3: 实现后台统计与预约处理**

```python
@admin_bp.route("/appointments", methods=["GET", "POST"])
@admin_login_required
def appointments():
    if request.method == "POST":
        appointment = Appointment.query.get_or_404(int(request.form["appointment_id"]))
        appointment.status = request.form["status"]
        db.session.commit()
```

- [ ] **Step 4: 实现大屏脱敏聚合**

```python
return {
    "kpis": {...},
    "emotion_counts": emotion_counts,
    "scale_stats": scale_stats,
    "schedule_hotspots": hotspot_list,
}
```

- [ ] **Step 5: 重新运行测试**

Run: `pytest tests/test_admin_and_screen.py -q`
Expected: 后台与大屏测试通过。

### Task 4: 完成 SQL 与部署基础

**Files:**
- Create: `sql/schema.sql`
- Create: `sql/seed.sql`
- Create: `docs/deployment-guide.md`
- Create: `docs/database-design.md`

- [ ] **Step 1: 写 SQL 文件存在性与关键表测试**

```python
def test_schema_sql_contains_required_tables():
    content = Path("sql/schema.sql").read_text(encoding="utf-8")
    assert "CREATE TABLE users" in content
    assert "CREATE TABLE appointments" in content
```

- [ ] **Step 2: 运行测试确认失败**

Run: `pytest tests -q`
Expected: 缺少 SQL 文件或缺少建表语句导致失败。

- [ ] **Step 3: 编写建表和初始化脚本**

```sql
CREATE TABLE users (
  id INT PRIMARY KEY AUTO_INCREMENT,
  student_no VARCHAR(20) NOT NULL UNIQUE,
  ...
);
```

- [ ] **Step 4: 编写部署与数据库说明**

```markdown
1. 安装 Python 3.13
2. 执行 `pip install -r requirements.txt`
3. 在 MySQL 中执行 `sql/schema.sql` 与 `sql/seed.sql`
4. 配置 `.env`
5. 运行 `python run.py`
```

- [ ] **Step 5: 重新运行测试**

Run: `pytest tests -q`
Expected: SQL 相关检查通过。

### Task 5: 完成交付文档管理与课程报告草稿

**Files:**
- Create: `docs/test-report.md`
- Create: `docs/course-report-outline.md`
- Create: `docs/assets/README.md`
- Modify: `docs/superpowers/specs/2026-06-26-mental-health-system-design.md`

- [ ] **Step 1: 写文档交付清单检查**

```python
def test_required_docs_exist():
    assert Path("docs/deployment-guide.md").exists()
    assert Path("docs/database-design.md").exists()
    assert Path("docs/course-report-outline.md").exists()
```

- [ ] **Step 2: 运行测试确认失败**

Run: `pytest tests -q`
Expected: 文档缺失测试失败。

- [ ] **Step 3: 编写文档骨架**

```markdown
# 课程报告草稿提纲
## 第一章 系统需求分析
## 第二章 可行性分析
## 第三章 概要设计
## 第四章 系统详细设计与实现
## 第五章 系统测试
## 第六章 总结与展望
```

- [ ] **Step 4: 编写测试记录与素材说明**

```markdown
- 截图 1：学生端首页
- 截图 2：测评结果页
- 截图 3：树洞页
- 截图 4：后台统计页
- 截图 5：大屏看板
```

- [ ] **Step 5: 重新运行测试**

Run: `pytest tests -q`
Expected: 文档存在性检查通过。

### Task 6: 最终联调与验收

**Files:**
- Modify: `tests/test_app_factory.py`
- Modify: `tests/test_student_routes.py`
- Modify: `tests/test_admin_and_screen.py`
- Modify: `docs/test-report.md`

- [ ] **Step 1: 增加最终烟测**

```python
def test_home_route_responds_successfully():
    response = client.get("/")
    assert response.status_code == 200
```

- [ ] **Step 2: 运行完整测试确认现状**

Run: `pytest tests -q`
Expected: 若还有失败，精确定位未完成模块。

- [ ] **Step 3: 修正剩余问题并更新测试记录**

```markdown
- 功能测试：注册、登录、测评、树洞、预约、后台、大屏
- 性能测试：首页、测评页、看板页加载时间
- 兼容性测试：手机端、桌面端、大屏端
```

- [ ] **Step 4: 运行最终完整测试**

Run: `pytest tests -q`
Expected: 所有测试通过，输出无收集错误。

- [ ] **Step 5: 手工烟测**

Run: `python run.py`
Expected: 本地服务可启动，学生端、后台端和大屏端可访问。
