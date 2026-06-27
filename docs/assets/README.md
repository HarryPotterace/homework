# 报告素材清单

## 1. 必备素材
- 学生端首页截图。
- 测评页截图。
- 测评结果页截图。
- 匿名树洞页截图。
- 情绪感知交互页截图。
- 预约页截图。
- 后台总览页截图。
- 后台记录页截图。
- 大屏看板截图。
- 系统流程图。
- ER 图。
- 类谱系树。
- 测试结果表格。

## 2. 用途
- 所有素材都需要在课程报告中按章节使用，并配图号或表号。
- 素材建议与报告章节的对应关系如下：
  - 第一章 / 第三章：系统流程图、类谱系树
  - 第四章：学生端、后台端、大屏端界面截图，ER 图
  - 第五章：测试结果表格、兼容性与性能测试截图

## 3. 建议命名
- `fig-01-student-home.png`
- `fig-02-assessment-form.png`
- `fig-03-assessment-result.png`
- `fig-04-vent-page.png`
- `fig-05-emotion-page.png`
- `fig-06-appointments-page.png`
- `fig-07-admin-dashboard.png`
- `fig-08-admin-records.png`
- `fig-09-screen-dashboard.png`
- `fig-10-system-flow.png`
- `fig-11-er-diagram.png`
- `fig-12-class-tree.png`
- `tab-01-functional-tests.xlsx` 或等效图片

## 4. 当前素材源文件
- `docs/assets/system-flow.md`
  - 系统流程图 Mermaid 源文件。
- `docs/assets/er-diagram.md`
  - 数据库 ER 图 Mermaid 源文件。
- `docs/assets/class-tree.md`
  - 类谱系树 Mermaid 源文件。
- `docs/assets/capture-checklist.md`
  - 页面截图、测试附件和导出顺序清单。
- `docs/assets/test-evidence/`
  - 自动化测试原始输出留档。

## 5. 当前状态
- 命名规范和用途已确定。
- 三张结构图的源码已经生成，待导出成图片。
- 已补统一版关键页面截图：
  - `docs/assets/screenshots/fig-01-student-home.png`
  - `docs/assets/screenshots/fig-07-admin-dashboard.png`
  - `docs/assets/screenshots/fig-09-screen-dashboard.png`
- 已补自动化测试文本证据：
  - `docs/assets/test-evidence/pytest-integrated-ui-2026-06-27.txt`
  - `docs/assets/test-evidence/pytest-full-2026-06-27.txt`
- 剩余页面截图和终端截图仍需在最终演示环境中人工采集。
- 测试表格已经在 `docs/test-report.md` 形成底稿，可直接转成报告表格。
