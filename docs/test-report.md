# 系统测试记录

## 1. 文档用途
- 记录自动化测试、人工功能测试、性能测试、兼容性测试及结果分析。
- 本文作为课程报告第五章“系统测试”的底稿。

## 2. 测试任务
- 验证学生端主流程是否可用。
- 验证后台端与大屏端是否可访问并满足脱敏要求。
- 验证 SQL 资源、情绪规则、量表评分逻辑是否可回归。
- 为课程报告提供测试表格、结果和分析依据。

## 3. 测试目标
- 功能正确：注册、登录、测评、树洞、行为采集、预约、后台处理、大屏展示全部可用。
- 结果可解释：量表得分、情绪标签、预约状态变化具备明确规则。
- 页面可访问：手机端、PC 后台、大屏端均能完成对应任务。
- 数据合规：树洞匿名，大屏只展示聚合数据。

## 4. 测试方案

### 4.1 自动化测试
- 统一命令：`python -m pytest -q`
- 当前测试文件：
  - `tests/test_app_factory.py`
  - `tests/test_services.py`
  - `tests/test_student_routes.py`
  - `tests/test_admin_and_screen.py`
  - `tests/test_sql_assets.py`
  - `tests/test_backend_modernization.py`
  - `tests/test_mysql_and_integrated_ui.py`

### 4.2 人工流程测试
按三端实际操作路径执行：

1. 学生注册并登录。
2. 修改个人资料。
3. 完成一次量表测评。
4. 发布一次匿名树洞。
5. 在情绪感知页触发行为采集。
6. 创建并取消一次预约。
7. 后台登录并查看统计、记录、预约。
8. 打开大屏并检查是否为脱敏聚合展示。

### 4.3 性能测试口径
- 首页首次加载时间。
- 测评页提交到结果展示耗时。
- 大屏页首次渲染时间。

### 4.4 兼容性测试口径
- 学生端：手机宽度下可完整使用。
- 后台端：Chrome / Edge 下表格和导航可用。
- 大屏端：`1920x1080` 下全屏展示可读。

## 5. 当前自动化测试结果

### 5.1 当前结果
截至 `2026-06-27` 统一集成分支 `feat/backend-core`，执行：

```powershell
python -m pytest -q tests/test_mysql_and_integrated_ui.py
python -m pytest -q
```

结果为：
- 集成回归测试：`5 passed`
- 全量自动化测试：`40 passed`
- 说明：学生端优化页、后台统一版、看板页和 MySQL-only 运行时约束已合并到同一 Flask 服务内验证，不再存在分支间双版本页面。

### 5.2 集成与运行时证据
- 统一服务访问地址：`http://127.0.0.1:5000/`
- 已验证页面：`/`、`/admin/login`、`/screen`
- 运行数据库：MySQL，`127.0.0.1:3307`
- 环境变量：`.env` 指向 `mysql+pymysql://mental_app:***@127.0.0.1:3307/mental_health_system?charset=utf8mb4`
- 运行时约束：非测试环境若未配置 `DATABASE_URL` 或不是 `mysql+pymysql://...`，应用启动即报错；测试环境仅允许显式注入测试数据库 URI
- 测试输出留档：
  - `docs/assets/test-evidence/pytest-integrated-ui-2026-06-27.txt`
  - `docs/assets/test-evidence/pytest-full-2026-06-27.txt`

### 5.3 覆盖内容

| 测试项 | 当前状态 | 对应测试 |
| --- | --- | --- |
| 应用工厂可正常创建应用 | 通过 | `test_app_factory.py` |
| 量表评分逻辑 | 通过 | `test_services.py` |
| 文本情绪规则 | 通过 | `test_services.py` |
| 行为情绪规则 | 通过 | `test_services.py` |
| 学生注册与登录 | 通过 | `test_student_routes.py` |
| 注册页校验脚本加载 | 通过 | `test_student_routes.py` |
| 预约时段异步接口 | 通过 | `test_student_routes.py` |
| 学生首页支持入口与个性化摘要 | 通过 | `test_student_routes.py` |
| 测评记录保存 | 通过 | `test_student_routes.py` |
| 树洞情绪标签生成 | 通过 | `test_student_routes.py` |
| 预约创建与取消 | 通过 | `test_student_routes.py` |
| 后台登录与总览访问 | 通过 | `test_admin_and_screen.py` |
| 后台工作台与图表钩子 | 通过 | `test_admin_and_screen.py` |
| 大屏 KPI / 图表 / 脱敏说明 | 通过 | `test_admin_and_screen.py` |
| SQL 表结构资源存在性 | 通过 | `test_sql_assets.py` |
| SQL 初始化数据存在性 | 通过 | `test_sql_assets.py` |
| 后端现代化保护项 | 通过 | `test_backend_modernization.py` |
| 统一版学生首页 UI | 通过 | `test_mysql_and_integrated_ui.py` |
| 统一版大屏看板 UI | 通过 | `test_mysql_and_integrated_ui.py` |
| MySQL-only 运行时限制 | 通过 | `test_mysql_and_integrated_ui.py` |
| 测试环境数据库覆盖行为 | 通过 | `test_mysql_and_integrated_ui.py` |

## 6. 人工功能测试表

| 编号 | 测试内容 | 预期结果 | 当前记录 |
| --- | --- | --- | --- |
| F-01 | 学生注册 | 学号唯一校验生效，注册成功后跳转登录 | 待录入截图 |
| F-02 | 学生登录 | 登录成功并创建 Session | 待录入截图 |
| F-03 | 个人信息修改 | 昵称与联系方式可更新 | 待录入截图 |
| F-04 | PHQ-9 / GAD-7 测评 | 计算得分、生成建议、记录入库 | 待录入截图 |
| F-05 | 匿名树洞发布 | 不展示身份信息，生成情绪标签 | 待录入截图 |
| F-06 | 学生首页支持入口 | 可直接进入测评、树洞、预约，并可见隐私说明 | 已采集 `fig-01-student-home.png` |
| F-07 | 情绪感知页 | 行为采集后显示情绪和界面模式 | 待录入截图 |
| F-08 | 预约创建与取消 | 预约成功并锁定时段，取消后释放时段 | 待录入截图 |
| F-09 | 后台总览工作台 | 可查看待处理预约、需关注树洞和图形化统计 | 已采集 `fig-07-admin-dashboard.png` |
| F-10 | 大屏展示 | 显示态势 KPI、图表和脱敏说明，不暴露身份字段 | 已采集 `fig-09-screen-dashboard.png` |

当前截图补证：
- 已采集统一版学生端首页：`docs/assets/screenshots/fig-01-student-home.png`
- 已采集统一版后台总览页：`docs/assets/screenshots/fig-07-admin-dashboard.png`
- 已采集统一版大屏看板页：`docs/assets/screenshots/fig-09-screen-dashboard.png`
- 已保存自动化测试输出：`docs/assets/test-evidence/pytest-full-2026-06-27.txt`

## 7. 性能测试记录

| 编号 | 页面/操作 | 测试环境 | 结果 | 结论 |
| --- | --- | --- | --- | --- |
| P-01 | 首页首次加载 | Windows 11 + Python 3.13 + Flask 测试客户端 + 隔离测试数据库 | 平均 `1.09 ms`，最小 `0.42 ms`，最大 `12.46 ms` | 本地渲染响应快 |
| P-02 | 测评提交到结果展示 | Windows 11 + Python 3.13 + Flask 测试客户端 + 隔离测试数据库 | 平均 `44.20 ms`，最小 `9.85 ms`，最大 `269.06 ms` | 含入库与结果计算，处于课程演示可接受范围 |
| P-03 | 大屏首屏渲染 | Windows 11 + Python 3.13 + Flask 测试客户端 + 隔离测试数据库 | 平均 `4.90 ms`，最小 `3.71 ms`，最大 `19.41 ms` | 聚合统计页本地响应稳定 |

性能测试说明：
- 测量方式：使用 Flask `test_client()` 对关键路由重复请求，首页和大屏各 20 次，测评提交 10 次。
- 测评页访问过程同时测得 `GET /assessment` 平均 `0.97 ms`，说明页面读取本身开销较低，主要耗时在提交后的数据库写入与结果渲染。
- 当前结果用于课程报告中的“本地开发环境性能基线”，不等同于公网部署性能。

## 8. 兼容性测试记录模板

| 编号 | 终端/浏览器 | 测试内容 | 结果 | 结论 |
| --- | --- | --- | --- | --- |
| C-01 | 手机端 Chrome | 学生端主流程 | 待测 | 待填写 |
| C-02 | PC Chrome | 后台端主流程 | 待测 | 待填写 |
| C-03 | PC Edge | 后台端主流程 | 待测 | 待填写 |
| C-04 | 1920x1080 大屏 | 看板展示可读性 | 待测 | 待填写 |

当前说明：
- 兼容性部分尚未形成实机截图证据，仍需要在手机 Chrome、PC Chrome、PC Edge 和 `1920x1080` 大屏环境下人工验证。
- 对应截图采集要求已整理到 `docs/assets/capture-checklist.md`。

## 9. 脱敏与交互检查
- 树洞页面默认匿名，不向学生侧显示学号、姓名。
- 大屏页面使用 `summary` 聚合结果，不直接输出用户身份字段。
- 情绪感知页根据行为规则返回 `平静 / 焦虑 / 低落` 和界面模式。

## 10. 后续待补内容
- 剩余页面截图：`fig-02` 到 `fig-06`、`fig-08`。
- 兼容性测试实测数据。
- 人工测试结果分析段落。
- `python -m pytest -q` 终端截图（当前已保留文本证据，截图待补）。
- `fig-10` 到 `fig-12` 结构图导出图片。
