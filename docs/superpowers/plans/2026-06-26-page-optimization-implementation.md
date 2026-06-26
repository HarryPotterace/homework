# Three-Key-Pages Optimization Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rebuild the student home page, admin dashboard, and screen dashboard into a unified, action-first experience that matches the page optimization spec while preserving the existing Flask monolith structure.

**Architecture:** Keep server-side rendering as the main delivery model, add only lightweight front-end behavior, and concentrate shared visual rules in `static/css/app.css`. Extend existing route summaries with focused page data instead of introducing a new API layer. Use route-level tests to lock the new information architecture with stable hooks such as section ids, data attributes, and page text.

**Tech Stack:** Flask, Jinja2, Bootstrap, custom CSS/JS, pytest

---

## File Structure

- `app/routes/student.py`
  - Extend the student home route to provide logged-in summary data for the personalized state block.
- `app/services/home.py`
  - New focused service for student home personalized summary so home-page logic does not bloat the route file.
- `app/services/dashboard.py`
  - Extend existing summary builders with processing-oriented data for admin and screen pages.
- `templates/base.html`
  - Add shared student mobile bottom navigation hook and page-level body classes if needed.
- `templates/student/home.html`
  - Full student home information architecture rewrite.
- `templates/admin/dashboard.html`
  - Replace passive totals-first layout with workbench-style layout.
- `templates/screen/index.html`
  - Replace list-heavy screen with KPI + chart/panel composition.
- `static/css/app.css`
  - Add shared page-optimization tokens, section layouts, state chips, chart shells, and responsive rules.
- `static/js/dashboard.js`
  - New lightweight chart/init script for admin dashboard.
- `static/js/screen.js`
  - New lightweight chart/init script for large screen dashboard.
- `tests/test_student_routes.py`
  - Add route assertions for the new student-home modules and logged-in summary block.
- `tests/test_admin_and_screen.py`
  - Add assertions for the admin workbench modules and screen dashboard modules.
- `docs/assets/capture-checklist.md`
  - Update screenshot descriptions after page structure changes.
- `docs/test-report.md`
  - Update manual test wording to reflect new page modules after implementation.

## Task 1: Add Shared Visual Hooks And Student Home Summary Service

**Files:**
- Create: `app/services/home.py`
- Modify: `app/routes/student.py`
- Modify: `templates/base.html`
- Modify: `static/css/app.css`
- Test: `tests/test_student_routes.py`

- [ ] **Step 1: Write the failing tests for the optimized student home shell**

```python
def test_home_page_prioritizes_support_actions():
    app = build_app()
    client = app.test_client()

    response = client.get("/")

    assert response.status_code == 200
    assert b'data-page="student-home"' in response.data
    assert "快速测评".encode("utf-8") in response.data
    assert "匿名倾诉".encode("utf-8") in response.data
    assert "预约咨询".encode("utf-8") in response.data
    assert b'id="support-paths"' in response.data


def test_logged_in_home_page_shows_personalized_summary():
    app = build_app()
    client = app.test_client()
    register_student(client)
    login_student(client)

    response = client.get("/")

    assert response.status_code == 200
    assert b'data-home-summary="true"' in response.data
    assert "最近一次测评".encode("utf-8") in response.data
    assert "最近预约状态".encode("utf-8") in response.data
```

- [ ] **Step 2: Run the targeted tests to verify they fail**

Run:

```powershell
python -m pytest tests/test_student_routes.py::test_home_page_prioritizes_support_actions tests/test_student_routes.py::test_logged_in_home_page_shows_personalized_summary -q
```

Expected:
- Both tests fail because the current home page lacks `data-page="student-home"`, `support-paths`, and personalized summary hooks.

- [ ] **Step 3: Add a focused student home summary service**

Create `app/services/home.py`:

```python
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

    return {
        "has_summary": bool(latest_assessment or latest_appointment),
        "latest_assessment": latest_assessment,
        "latest_appointment": latest_appointment,
        "recommended_action": (
            "继续查看测评建议"
            if latest_assessment
            else "先完成一次快速测评"
        ),
    }
```

- [ ] **Step 4: Wire the summary into the student home route**

Modify `app/routes/student.py` home route:

```python
from app.services.home import build_student_home_summary


@student_bp.route("/")
def home():
    home_summary = None
    if session.get("user_id"):
        home_summary = build_student_home_summary(session["user_id"])

    return render_template(
        "student/home.html",
        scales=get_scale_catalog(),
        home_summary=home_summary,
    )
```

- [ ] **Step 5: Add shared page-level hooks to the base layout**

Modify `templates/base.html`:

```html
<body class="{% block body_class %}{% endblock %}" data-page-shell="student-system">
  ...
  {% block mobile_nav %}{% endblock %}
  <script src="{{ url_for('static', filename='js/app.js') }}"></script>
```

Add a default mobile-nav block near the end of `base.html`:

```html
{% block mobile_nav %}
<nav class="mobile-tabbar d-lg-none" aria-label="学生快捷导航">
  <a href="{{ url_for('student.home') }}">首页</a>
  <a href="{{ url_for('student.assessment') }}">测评</a>
  <a href="{{ url_for('student.vent') }}">树洞</a>
  <a href="{{ url_for('student.appointments') }}">预约</a>
  <a href="{{ url_for('student.profile') if student_logged_in else url_for('student.login') }}">我的</a>
</nav>
{% endblock %}
```

- [ ] **Step 6: Add shared CSS primitives for the optimized pages**

Modify `static/css/app.css` with the new shared rules:

```css
:root {
  --calm-50: #f5fbfa;
  --calm-100: #e8f5f2;
  --calm-500: #247c8a;
  --calm-700: #14515b;
  --alert-500: #d38a2f;
  --risk-500: #b35757;
  --ink-900: #19343b;
  --muted-600: #5d787f;
}

.mobile-tabbar {
  position: sticky;
  bottom: 0;
  z-index: 1030;
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 0.25rem;
  padding: 0.6rem 0.75rem calc(0.75rem + env(safe-area-inset-bottom));
  background: rgba(255, 255, 255, 0.92);
  backdrop-filter: blur(18px);
  border-top: 1px solid rgba(36, 124, 138, 0.12);
}

.mobile-tabbar a {
  min-height: 44px;
  display: grid;
  place-items: center;
  border-radius: 999px;
  color: var(--muted-600);
  text-decoration: none;
}

.mobile-tabbar a:hover,
.mobile-tabbar a:focus-visible {
  background: var(--calm-100);
  color: var(--calm-700);
}
```

- [ ] **Step 7: Run the targeted tests to verify the new shell hooks pass**

Run:

```powershell
python -m pytest tests/test_student_routes.py::test_home_page_prioritizes_support_actions tests/test_student_routes.py::test_logged_in_home_page_shows_personalized_summary -q
```

Expected:
- PASS

- [ ] **Step 8: Commit**

```powershell
git add app/services/home.py app/routes/student.py templates/base.html static/css/app.css tests/test_student_routes.py
git commit -m "feat: add shared page hooks and student home summary"
```

## Task 2: Rebuild The Student Home Page Into An Action-First Support Entry

**Files:**
- Modify: `templates/student/home.html`
- Modify: `static/css/app.css`
- Test: `tests/test_student_routes.py`

- [ ] **Step 1: Write the failing tests for the new student home modules**

```python
def test_home_page_includes_support_path_cards():
    app = build_app()
    client = app.test_client()

    response = client.get("/")

    assert response.status_code == 200
    assert b'id="support-paths"' in response.data
    assert "最近压力有点大".encode("utf-8") in response.data
    assert "想先匿名说一说".encode("utf-8") in response.data


def test_home_page_includes_relief_and_privacy_sections():
    app = build_app()
    client = app.test_client()

    response = client.get("/")

    assert response.status_code == 200
    assert b'id="instant-relief"' in response.data
    assert b'id="trust-guardrails"' in response.data
    assert "仅展示脱敏汇总".encode("utf-8") in response.data
```

- [ ] **Step 2: Run the targeted tests to verify they fail**

Run:

```powershell
python -m pytest tests/test_student_routes.py::test_home_page_includes_support_path_cards tests/test_student_routes.py::test_home_page_includes_relief_and_privacy_sections -q
```

Expected:
- FAIL because the current template has no `support-paths`, `instant-relief`, or `trust-guardrails` sections.

- [ ] **Step 3: Replace the student home layout with the optimized section structure**

Modify `templates/student/home.html` to use this top-level structure:

```html
{% extends "base.html" %}

{% block body_class %}student-home-body{% endblock %}

{% block content %}
<section class="student-home-shell" data-page="student-home">
  <div class="container">
    <section class="student-hero panel-card">
      ...
    </section>

    <section id="support-paths" class="home-section">
      ...
    </section>

    <section id="quick-scales" class="home-section">
      ...
    </section>

    <section id="instant-relief" class="home-section">
      ...
    </section>

    <section id="trust-guardrails" class="home-section">
      ...
    </section>
  </div>
</section>
{% endblock %}
```

- [ ] **Step 4: Fill the hero and support-path modules with action-first content**

Use these concrete content blocks in `templates/student/home.html`:

```html
<div class="student-hero-copy">
  <span class="soft-badge">校园心理支持入口</span>
  <h1>如果你最近有点累，可以先从这里开始</h1>
  <p class="lead text-secondary">先做一个简短自测，或先匿名说一说，再决定是否预约咨询。</p>
  <div class="hero-actions">
    <a class="btn btn-primary btn-lg rounded-pill px-4" href="{{ url_for('student.assessment') }}">快速测评</a>
    <a class="btn btn-outline-primary btn-lg rounded-pill px-4" href="{{ url_for('student.vent') }}">匿名倾诉</a>
    <a class="btn btn-outline-primary btn-lg rounded-pill px-4" href="{{ url_for('student.appointments') }}">预约咨询</a>
  </div>
</div>

<div class="support-grid">
  <article class="support-card">
    <h2>最近压力有点大</h2>
    <p>先做一次简短测评，看看最近的压力和情绪状态。</p>
  </article>
  <article class="support-card">
    <h2>最近有些焦虑</h2>
    <p>从焦虑相关测评开始，再决定是否需要后续支持。</p>
  </article>
  <article class="support-card">
    <h2>想先匿名说一说</h2>
    <p>不用先解释身份，可以先把感受写下来。</p>
  </article>
  <article class="support-card">
    <h2>想直接预约咨询</h2>
    <p>查看可预约时段，尽快与咨询老师建立联系。</p>
  </article>
</div>
```

- [ ] **Step 5: Add personalized summary, quick scales, relief, and trust sections**

Use these template fragments:

```html
{% if home_summary %}
<section class="home-summary panel-card" data-home-summary="true">
  <h2>你的最近状态</h2>
  <div class="summary-grid">
    <article class="summary-item">
      <span>最近一次测评</span>
      <strong>{{ home_summary.latest_assessment.scale_name if home_summary.latest_assessment else "暂无记录" }}</strong>
    </article>
    <article class="summary-item">
      <span>最近预约状态</span>
      <strong>{{ home_summary.latest_appointment.status if home_summary.latest_appointment else "暂无预约" }}</strong>
    </article>
    <article class="summary-item">
      <span>推荐下一步</span>
      <strong>{{ home_summary.recommended_action }}</strong>
    </article>
  </div>
</section>
{% endif %}

<section id="instant-relief" class="home-section">
  <h2>先给自己一点缓冲</h2>
  <div class="relief-grid">
    <article class="relief-card"><h3>60 秒呼吸</h3><p>先慢下来，再决定下一步。</p></article>
    <article class="relief-card"><h3>写一句感受</h3><p>把此刻的情绪写出来，降低憋闷感。</p></article>
    <article class="relief-card"><h3>放松建议</h3><p>获取一条简单、可立即执行的建议。</p></article>
  </div>
</section>

<section id="trust-guardrails" class="home-section">
  <div class="trust-grid">
    <article class="trust-item">匿名发布不会在学生侧公开身份信息</article>
    <article class="trust-item">预约信息仅用于咨询服务安排</article>
    <article class="trust-item">大屏仅展示脱敏汇总，不展示个人身份</article>
  </div>
</section>
```

- [ ] **Step 6: Add student-home-specific CSS rules**

Append to `static/css/app.css`:

```css
.student-home-shell {
  padding-bottom: 5rem;
}

.student-hero,
.home-summary,
.home-section {
  margin-bottom: 1.5rem;
}

.hero-actions,
.support-grid,
.summary-grid,
.relief-grid,
.trust-grid {
  display: grid;
  gap: 1rem;
}

.hero-actions {
  grid-template-columns: repeat(3, minmax(0, auto));
  align-items: center;
}

.support-grid {
  grid-template-columns: repeat(2, minmax(0, 1fr));
}

.support-card,
.summary-item,
.relief-card,
.trust-item {
  background: #f8fcfb;
  border: 1px solid rgba(36, 124, 138, 0.08);
  border-radius: 24px;
  padding: 1.1rem;
}

@media (max-width: 767.98px) {
  .hero-actions,
  .support-grid,
  .summary-grid,
  .relief-grid,
  .trust-grid {
    grid-template-columns: 1fr;
  }
}
```

- [ ] **Step 7: Run the student route tests for the optimized home page**

Run:

```powershell
python -m pytest tests/test_student_routes.py -q
```

Expected:
- PASS

- [ ] **Step 8: Commit**

```powershell
git add templates/student/home.html static/css/app.css tests/test_student_routes.py
git commit -m "feat: redesign student home page"
```

## Task 3: Extend Dashboard Summary Data For Workbench And Screen Use

**Files:**
- Modify: `app/services/dashboard.py`
- Test: `tests/test_admin_and_screen.py`

- [ ] **Step 1: Write failing tests for processing-first dashboard data hooks**

```python
def test_admin_dashboard_exposes_workbench_sections():
    app = build_app()
    client = app.test_client()

    response = client.post(
        "/admin/login",
        data={"username": "admin", "password": "Admin12345"},
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b'data-page="admin-dashboard"' in response.data
    assert "待确认预约".encode("utf-8") in response.data
    assert "需关注树洞".encode("utf-8") in response.data


def test_screen_page_exposes_kpi_and_focus_panels():
    app = build_app()
    client = app.test_client()

    response = client.get("/screen")

    assert response.status_code == 200
    assert b'data-page="screen-dashboard"' in response.data
    assert "当前需关注人数".encode("utf-8") in response.data
    assert "仅展示脱敏聚合数据".encode("utf-8") in response.data
```

- [ ] **Step 2: Run the targeted admin/screen tests to verify they fail**

Run:

```powershell
python -m pytest tests/test_admin_and_screen.py::test_admin_dashboard_exposes_workbench_sections tests/test_admin_and_screen.py::test_screen_page_exposes_kpi_and_focus_panels -q
```

Expected:
- FAIL because the templates do not yet include the new workbench/screen hooks.

- [ ] **Step 3: Extend `build_dashboard_summary()` with processing-oriented fields**

Modify `app/services/dashboard.py`:

```python
def build_dashboard_summary():
    ...
    pending_appointments = Appointment.query.filter_by(status="待确认").count()
    attention_posts = VentPost.query.filter_by(emotion="需关注").count()
    recent_assessments = (
        AssessmentRecord.query.order_by(AssessmentRecord.created_at.desc()).limit(5).all()
    )
    recent_attention_posts = (
        VentPost.query.order_by(VentPost.created_at.desc()).limit(5).all()
    )
    recent_appointments = (
        Appointment.query.order_by(Appointment.created_at.desc()).limit(5).all()
    )

    return {
        "kpis": {...},
        "workbench": {
            "pending_appointments": pending_appointments,
            "attention_posts": attention_posts,
            "recent_assessments": recent_assessments,
            "recent_attention_posts": recent_attention_posts,
            "recent_appointments": recent_appointments,
        },
        "emotion_counts": emotion_counts,
        "scale_stats": scale_stats,
        "schedule_hotspots": [...],
        "screen_focus": {
            "attention_total": emotion_counts.get("需关注", 0),
            "weekly_assessments": total_assessments,
            "weekly_appointments": total_appointments,
            "vent_activity": total_posts,
        },
    }
```

- [ ] **Step 4: Keep naming and summary boundaries explicit**

Refine the final summary structure in `app/services/dashboard.py` so template consumers can rely on stable keys:

```python
summary = build_dashboard_summary()
summary["workbench"]["recent_appointments"]
summary["screen_focus"]["attention_total"]
summary["emotion_counts"]
summary["scale_stats"]
summary["schedule_hotspots"]
```

Do not add a second overlapping summary builder unless one page truly needs incompatible structure.

- [ ] **Step 5: Run the focused tests to verify the data shape supports later template work**

Run:

```powershell
python -m pytest tests/test_admin_and_screen.py::test_admin_dashboard_exposes_workbench_sections tests/test_admin_and_screen.py::test_screen_page_exposes_kpi_and_focus_panels -q
```

Expected:
- Still FAIL on template text/hooks, but no new backend error should appear in logs.

- [ ] **Step 6: Commit**

```powershell
git add app/services/dashboard.py tests/test_admin_and_screen.py
git commit -m "feat: extend dashboard summary for optimized pages"
```

## Task 4: Rebuild The Admin Dashboard Into A Processing Workbench

**Files:**
- Modify: `templates/admin/dashboard.html`
- Modify: `templates/admin/base.html`
- Modify: `static/css/app.css`
- Create: `static/js/dashboard.js`
- Test: `tests/test_admin_and_screen.py`

- [ ] **Step 1: Write failing tests for admin dashboard sections and quick actions**

```python
def test_admin_dashboard_includes_workbench_queues():
    app = build_app()
    client = app.test_client()
    client.post("/admin/login", data={"username": "admin", "password": "Admin12345"}, follow_redirects=True)

    response = client.get("/admin/dashboard")

    assert response.status_code == 200
    assert b'id="admin-workbench"' in response.data
    assert "待处理预约".encode("utf-8") in response.data
    assert "近期异常情绪记录".encode("utf-8") in response.data


def test_admin_dashboard_includes_chart_hooks():
    app = build_app()
    client = app.test_client()
    client.post("/admin/login", data={"username": "admin", "password": "Admin12345"}, follow_redirects=True)

    response = client.get("/admin/dashboard")

    assert response.status_code == 200
    assert b'id="emotion-distribution-chart"' in response.data
    assert b'data-dashboard-series=' in response.data
```

- [ ] **Step 2: Run the targeted tests to verify they fail**

Run:

```powershell
python -m pytest tests/test_admin_and_screen.py::test_admin_dashboard_includes_workbench_queues tests/test_admin_and_screen.py::test_admin_dashboard_includes_chart_hooks -q
```

Expected:
- FAIL because the current admin dashboard has no workbench queue or chart hooks.

- [ ] **Step 3: Replace the admin dashboard layout with the optimized module structure**

Modify `templates/admin/dashboard.html`:

```html
{% extends "admin/base.html" %}

{% block title %}后台总览{% endblock %}

{% block admin_content %}
<section class="admin-dashboard-shell" data-page="admin-dashboard">
  <section class="admin-kpi-grid">
    ...
  </section>

  <section id="admin-workbench" class="admin-workbench-grid">
    ...
  </section>

  <section class="admin-analysis-grid">
    ...
  </section>
</section>
{% endblock %}
```

- [ ] **Step 4: Fill the KPI and queue modules with processing-first content**

Use this structure in `templates/admin/dashboard.html`:

```html
<div class="metric-card">
  <span>待确认预约</span>
  <strong>{{ summary.workbench.pending_appointments }}</strong>
</div>
<div class="metric-card">
  <span>近 24 小时新增测评</span>
  <strong>{{ summary.workbench.recent_assessments|length }}</strong>
</div>
<div class="metric-card">
  <span>需关注树洞</span>
  <strong>{{ summary.workbench.attention_posts }}</strong>
</div>
<div class="metric-card">
  <span>近 7 天需关注人数</span>
  <strong>{{ summary.screen_focus.attention_total }}</strong>
</div>

<article class="panel-card">
  <div class="section-heading">
    <h2>待处理预约</h2>
    <a href="{{ url_for('admin.appointments') }}">进入预约处理</a>
  </div>
  ...
</article>

<article class="panel-card">
  <div class="section-heading">
    <h2>需关注树洞</h2>
    <a href="{{ url_for('admin.vents') }}">查看树洞记录</a>
  </div>
  ...
</article>

<article class="panel-card">
  <div class="section-heading">
    <h2>近期异常情绪记录</h2>
    <a href="{{ url_for('admin.assessments') }}">查看测评记录</a>
  </div>
  ...
</article>
```

- [ ] **Step 5: Add chart hooks and dashboard script loading**

Append to `templates/admin/dashboard.html`:

```html
<article class="panel-card">
  <h2>情绪分布</h2>
  <div
    id="emotion-distribution-chart"
    data-dashboard-series='{{ summary.emotion_counts|tojson }}'
  ></div>
</article>

<article class="panel-card">
  <h2>量表使用情况</h2>
  <div
    id="scale-usage-chart"
    data-dashboard-series='{{ summary.scale_stats|tojson }}'
  ></div>
</article>
{% block scripts %}
{{ super() }}
<script src="{{ url_for('static', filename='js/dashboard.js') }}"></script>
{% endblock %}
```

Create `static/js/dashboard.js`:

```javascript
function renderSimpleBars(containerId) {
  const container = document.getElementById(containerId);
  if (!container) return;
  const payload = JSON.parse(container.dataset.dashboardSeries || "{}");
  const entries = Object.entries(payload);
  const max = Math.max(...entries.map(([, value]) => value), 1);

  container.innerHTML = entries
    .map(
      ([label, value]) => `
        <div class="mini-bar-row">
          <span>${label}</span>
          <div class="mini-bar-track"><div class="mini-bar-fill" style="width:${(value / max) * 100}%"></div></div>
          <strong>${value}</strong>
        </div>
      `
    )
    .join("");
}

renderSimpleBars("emotion-distribution-chart");
renderSimpleBars("scale-usage-chart");
```

- [ ] **Step 6: Add admin-workbench CSS rules**

Append to `static/css/app.css`:

```css
.admin-dashboard-shell,
.admin-kpi-grid,
.admin-workbench-grid,
.admin-analysis-grid {
  display: grid;
  gap: 1rem;
}

.admin-kpi-grid {
  grid-template-columns: repeat(4, minmax(0, 1fr));
}

.admin-workbench-grid,
.admin-analysis-grid {
  grid-template-columns: repeat(3, minmax(0, 1fr));
  margin-top: 1rem;
}

.section-heading {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 0.75rem;
}

.mini-bar-row {
  display: grid;
  grid-template-columns: 96px 1fr auto;
  gap: 0.75rem;
  align-items: center;
  margin-bottom: 0.75rem;
}

.mini-bar-track {
  height: 10px;
  background: rgba(36, 124, 138, 0.08);
  border-radius: 999px;
  overflow: hidden;
}

.mini-bar-fill {
  height: 100%;
  border-radius: inherit;
  background: linear-gradient(135deg, var(--calm-500), var(--calm-700));
}
```

- [ ] **Step 7: Run the admin/screen test file**

Run:

```powershell
python -m pytest tests/test_admin_and_screen.py -q
```

Expected:
- PASS

- [ ] **Step 8: Commit**

```powershell
git add templates/admin/base.html templates/admin/dashboard.html static/css/app.css static/js/dashboard.js tests/test_admin_and_screen.py
git commit -m "feat: redesign admin dashboard as workbench"
```

## Task 5: Rebuild The Screen Dashboard Into A Readable Situation Board

**Files:**
- Modify: `templates/screen/index.html`
- Modify: `static/css/app.css`
- Create: `static/js/screen.js`
- Test: `tests/test_admin_and_screen.py`

- [ ] **Step 1: Write failing tests for the optimized screen dashboard**

```python
def test_screen_page_includes_focus_kpis_and_timestamp():
    app = build_app()
    client = app.test_client()

    response = client.get("/screen")

    assert response.status_code == 200
    assert b'id="screen-kpis"' in response.data
    assert "本周测评人数".encode("utf-8") in response.data
    assert "数据更新时间".encode("utf-8") in response.data


def test_screen_page_includes_focus_and_chart_sections():
    app = build_app()
    client = app.test_client()

    response = client.get("/screen")

    assert response.status_code == 200
    assert b'id="screen-focus-panel"' in response.data
    assert b'id="screen-emotion-chart"' in response.data
    assert "仅展示脱敏聚合数据".encode("utf-8") in response.data
```

- [ ] **Step 2: Run the targeted tests to verify they fail**

Run:

```powershell
python -m pytest tests/test_admin_and_screen.py::test_screen_page_includes_focus_kpis_and_timestamp tests/test_admin_and_screen.py::test_screen_page_includes_focus_and_chart_sections -q
```

Expected:
- FAIL because the current screen page lacks the new sections and ids.

- [ ] **Step 3: Replace the screen page structure with KPI + focus + chart modules**

Modify `templates/screen/index.html`:

```html
<body class="screen-body" data-page="screen-dashboard">
  <main class="screen-shell">
    <header class="screen-header">
      ...
    </header>

    <section id="screen-kpis" class="screen-grid">
      ...
    </section>

    <section class="screen-stage-grid">
      <article id="screen-emotion-chart" class="screen-panel" ...></article>
      <article id="screen-appointment-chart" class="screen-panel" ...></article>
      <article id="screen-scale-chart" class="screen-panel" ...></article>
    </section>

    <section id="screen-focus-panel" class="screen-focus-grid">
      ...
    </section>
  </main>
  <script src="{{ url_for('static', filename='js/screen.js') }}"></script>
</body>
```

- [ ] **Step 4: Fill the KPI, timestamp, and focus modules**

Use this content in `templates/screen/index.html`:

```html
<header class="screen-header">
  <div>
    <p class="screen-kicker">Campus Wellbeing Situation Board</p>
    <h1>学院心理态势脱敏数据看板</h1>
    <p class="screen-clock">数据更新时间：{{ summary.schedule_hotspots[-1].date if summary.schedule_hotspots else "当前会话" }}</p>
  </div>
  <div class="screen-note">仅展示脱敏聚合数据，不展示个人身份信息</div>
</header>

<article class="screen-card screen-card-risk">
  <span>当前需关注人数</span>
  <strong>{{ summary.screen_focus.attention_total }}</strong>
</article>
<article class="screen-card">
  <span>本周测评人数</span>
  <strong>{{ summary.screen_focus.weekly_assessments }}</strong>
</article>
<article class="screen-card">
  <span>本周预约人数</span>
  <strong>{{ summary.screen_focus.weekly_appointments }}</strong>
</article>
<article class="screen-card">
  <span>匿名表达活跃度</span>
  <strong>{{ summary.screen_focus.vent_activity }}</strong>
</article>

<section id="screen-focus-panel" class="screen-focus-grid">
  <article class="screen-panel">
    <h2>重点提示</h2>
    <ul>
      <li><span>需关注占比</span><strong>{{ summary.screen_focus.attention_total }}</strong></li>
      <li><span>当前预约热度</span><strong>{{ summary.kpis.appointments }}</strong></li>
      <li><span>匿名表达活跃度</span><strong>{{ summary.kpis.posts }}</strong></li>
    </ul>
  </article>
</section>
```

- [ ] **Step 5: Add screen chart hooks and initialization script**

Create `static/js/screen.js`:

```javascript
function renderScreenBars(containerId, dataAttribute) {
  const container = document.getElementById(containerId);
  if (!container) return;
  const payload = JSON.parse(container.dataset[dataAttribute] || "{}");
  const entries = Array.isArray(payload)
    ? payload.map((item) => [item.date, item.count])
    : Object.entries(payload);
  const max = Math.max(...entries.map(([, value]) => value), 1);

  container.innerHTML = entries
    .map(
      ([label, value]) => `
        <div class="screen-bar-row">
          <span>${label}</span>
          <div class="screen-bar-track"><div class="screen-bar-fill" style="width:${(value / max) * 100}%"></div></div>
          <strong>${value}</strong>
        </div>
      `
    )
    .join("");
}

renderScreenBars("screen-emotion-chart", "emotionSeries");
renderScreenBars("screen-appointment-chart", "appointmentSeries");
renderScreenBars("screen-scale-chart", "scaleSeries");
```

Attach these data attributes in `templates/screen/index.html`:

```html
<article id="screen-emotion-chart" class="screen-panel" data-emotion-series='{{ summary.emotion_counts|tojson }}'></article>
<article id="screen-appointment-chart" class="screen-panel" data-appointment-series='{{ summary.schedule_hotspots|tojson }}'></article>
<article id="screen-scale-chart" class="screen-panel" data-scale-series='{{ summary.scale_stats|tojson }}'></article>
```

- [ ] **Step 6: Add screen-specific CSS for readability**

Append to `static/css/app.css`:

```css
.screen-stage-grid,
.screen-focus-grid {
  display: grid;
  gap: 1.25rem;
  margin-top: 1.25rem;
}

.screen-stage-grid {
  grid-template-columns: repeat(3, minmax(0, 1fr));
}

.screen-focus-grid {
  grid-template-columns: 1fr;
}

.screen-card-risk strong,
.screen-note {
  color: #ffd7d7;
}

.screen-bar-row {
  display: grid;
  grid-template-columns: 108px 1fr auto;
  gap: 0.75rem;
  align-items: center;
  margin-bottom: 0.85rem;
}

.screen-bar-track {
  height: 12px;
  border-radius: 999px;
  overflow: hidden;
  background: rgba(255, 255, 255, 0.08);
}

.screen-bar-fill {
  height: 100%;
  border-radius: inherit;
  background: linear-gradient(135deg, #55c6d8, #e48f58);
}
```

- [ ] **Step 7: Run the admin/screen test file**

Run:

```powershell
python -m pytest tests/test_admin_and_screen.py -q
```

Expected:
- PASS

- [ ] **Step 8: Commit**

```powershell
git add templates/screen/index.html static/css/app.css static/js/screen.js tests/test_admin_and_screen.py
git commit -m "feat: redesign screen dashboard"
```

## Task 6: Align Docs, Screenshot Inventory, And Final Verification

**Files:**
- Modify: `docs/assets/capture-checklist.md`
- Modify: `docs/test-report.md`
- Test: `tests/test_student_routes.py`
- Test: `tests/test_admin_and_screen.py`

- [ ] **Step 1: Write failing assertions for any newly required route hooks if coverage is still missing**

If the previous tasks introduced untested ids or data attributes, add them before final verification:

```python
def test_screen_page_keeps_desensitized_notice():
    app = build_app()
    client = app.test_client()

    response = client.get("/screen")

    assert "不展示个人身份信息".encode("utf-8") in response.data
```

- [ ] **Step 2: Run the full focused route suite**

Run:

```powershell
python -m pytest tests/test_student_routes.py tests/test_admin_and_screen.py -q
```

Expected:
- PASS

- [ ] **Step 3: Update screenshot inventory wording**

Modify `docs/assets/capture-checklist.md` entries to match the optimized pages:

```markdown
| 1 | `fig-01-student-home.png` | 学生端首页（支持入口 + 支持类型卡） | `/` | 否 | 第四章 | 待人工截图 |
| 7 | `fig-07-admin-dashboard.png` | 后台总览页（待办工作台 + 图形化统计） | `/admin/dashboard` | 后台登录 | 第四章 | 待人工截图 |
| 9 | `fig-09-screen-dashboard.png` | 大屏看板页（KPI + 态势图表 + 脱敏说明） | `/screen` | 否 | 第四章 | 待人工截图 |
```

- [ ] **Step 4: Update manual test wording in `docs/test-report.md`**

Use the revised language:

```markdown
| F-06 | 学生首页支持入口 | 可直接进入测评、树洞、预约，并可见隐私说明 | 待录入截图 |
| F-09 | 后台总览工作台 | 可查看待处理预约、需关注树洞和图形化统计 | 待录入截图 |
| F-10 | 大屏展示 | 显示态势 KPI、图表和脱敏说明，不暴露身份字段 | 待录入截图 |
```

- [ ] **Step 5: Run the full project verification**

Run:

```powershell
python -m pytest -q
```

Expected:
- PASS with all tests green.

- [ ] **Step 6: Commit**

```powershell
git add docs/assets/capture-checklist.md docs/test-report.md tests/test_student_routes.py tests/test_admin_and_screen.py
git commit -m "docs: align evidence for optimized key pages"
```

## Self-Review

### 1. Spec coverage
- Student home information architecture: covered in Task 1 and Task 2.
- Admin dashboard workbench conversion: covered in Task 3 and Task 4.
- Screen board readability and desensitized focus: covered in Task 3 and Task 5.
- Unified visual language and shared hooks: covered in Task 1 and reinforced in Tasks 2, 4, and 5.
- Screenshot/test-doc alignment: covered in Task 6.

### 2. Placeholder scan
- No `TODO`, `TBD`, or "similar to above" references remain.
- Each task lists exact files, commands, expected outcomes, and concrete code fragments.

### 3. Type consistency
- Student home summary key is `home_summary`.
- Shared dashboard summary keys are `workbench`, `screen_focus`, `emotion_counts`, `scale_stats`, and `schedule_hotspots`.
- Route tests consistently assert `data-page="student-home"`, `data-page="admin-dashboard"`, and `data-page="screen-dashboard"`.

## Execution Handoff

Plan complete and saved to `docs/superpowers/plans/2026-06-26-page-optimization-implementation.md`. Two execution options:

**1. Subagent-Driven (recommended)** - I dispatch a fresh subagent per task, review between tasks, fast iteration

**2. Inline Execution** - Execute tasks in this session using executing-plans, batch execution with checkpoints

Which approach?
