# 作业要求覆盖审计

## 1. 输入材料
- `2025-2026学年第2学期《人机交互技术及应用》课程大作业.doc`
- `2025-2026学年第2学期《人机交互技术及应用》大作业评分标准.doc`
- `期末考试说明.pptx`

## 2. 要求覆盖表

| 要求 | 当前状态 | 对应文档/实现 |
| --- | --- | --- |
| B/S 结构系统 | 已锁定 | `docs/superpowers/specs/2026-06-26-mental-health-system-design.md` |
| 支持学生手机端、咨询师/管理员 PC 端、大屏看板 | 已实现主干，待联调验收 | `templates/student/`、`templates/admin/`、`templates/screen/` |
| 注册/登录/个人信息 | 已实现并有测试 | `app/routes/student.py`、`tests/test_student_routes.py` |
| 心理测评 | 已实现并有测试 | `app/services/assessment.py`、`app/routes/student.py`、`tests/test_student_routes.py` |
| 情绪感知与自适应交互 | 已实现轻量规则版，已补报告写作依据入口 | `static/js/behavior.js`、`app/services/emotion.py`、`app/routes/api.py`、`docs/course-report-outline.md` |
| 心理咨询预约 | 已实现并有测试 | `app/routes/student.py`、`app/routes/admin.py`、`app/routes/api.py` |
| 移动端响应式适配 | 已完成学生端一轮样式优化，待人工多端验收 | `static/css/app.css`、`templates/student/*.html` |
| 前端 JS 非空校验与密码强度校验 | 已实现并有测试 | `static/js/validation.js`、`tests/test_student_routes.py` |
| Session 登录管理 | 已实现，待人工联调复核 | `app/routes/student.py`、`app/routes/admin.py` |
| 行为采集 move/click/keydown | 已实现，待人工联调复核 | `static/js/behavior.js` |
| 预约 AJAX 获取/校验时段 | 已实现异步获取，前端可加载时段 | `app/routes/api.py`、`static/js/schedules.js` |
| 报告章节结构 | 已细化到章节级写作提纲 | `docs/course-report-outline.md` |
| 报告格式要求 | 已整理到可直接照写的底稿 | `docs/course-report-outline.md` |
| 研究背景、现状、方法与创新、结果分析、心得 | 已锁定写作边界，待转写为正式 Word 正文 | `docs/course-report-outline.md` |
| 参考文献与算法依据 | 未完成 | 需补充到 `docs/course-report-outline.md` 与设计说明 |
| 类谱系树及其说明 | 已生成源文件，待导出图片 | `docs/assets/class-tree.md` |
| 系统流程图、ER 图、界面截图 | 流程图和 ER 图源文件已生成，界面截图待人工采集 | `docs/assets/system-flow.md`、`docs/assets/er-diagram.md`、`docs/assets/capture-checklist.md` |
| 性能测试与兼容性测试 | 性能已补本地实测数据，兼容性待实机验证 | `docs/test-report.md` |
| 文件夹命名规则与截止时间 | 已锁定为终稿必检项 | `docs/course-report-outline.md` |
| 完整工程源码 + 系统配置说明书 + 数据库 SQL | 已形成可交付底稿，待最终打包 | `app/`、`sql/`、`docs/deployment-guide.md`、`docs/database-design.md` |

## 3. 当前结论
- 现有技术路线没有偏离老师原始要求，三端、核心功能、Session、前端校验、行为采集和预约异步接口都已经覆盖到代码层。
- 当前主要缺口不在功能主干，而在“最终交付闭环”：
  - 正式 `Word` 报告正文尚未完成。
  - 参考文献、方法依据、创新点和结果分析尚未转写成正式正文。
  - 结构图源文件已生成，但尚未导出为报告插图。
  - 页面截图和终端测试截图仍未人工采集。
  - 兼容性测试尚未执行实机验证。
  - 部署说明和数据库说明已经具备正式底稿，但还需要随最终实现做最后一次校订。

## 4. 编码前后都必须持续维护的检查项
- 若新增功能或改动数据库字段，先改设计说明和要求审计，再改代码。
- 若页面结构变化，必须同步检查截图素材清单和报告提纲。
- 若测试结果变化，必须同步更新 `docs/test-report.md`。
- 提交给老师前，必须把仓库底稿内容回填成一个正式 `Word` 报告，并按 `班级-姓名-学号` 命名最终文件夹。
