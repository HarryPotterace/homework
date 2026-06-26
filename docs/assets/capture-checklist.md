# 截图与证据采集清单

## 1. 用途
- 统一管理最终课程报告需要的截图、导出图和测试附件。
- 防止最后阶段重复截图、漏截图或命名不一致。

## 2. 页面截图清单

| 编号 | 建议文件名 | 页面/证据 | 访问路径 | 登录要求 | 报告章节 | 当前状态 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | `fig-01-student-home.png` | 学生端首页 | `/` | 否 | 第四章 | 待人工截图 |
| 2 | `fig-02-assessment-form.png` | 测评答题页 | `/assessment?scale=PHQ-9` | 学生登录 | 第四章 | 待人工截图 |
| 3 | `fig-03-assessment-result.png` | 测评结果页 | `/assessment` 提交后 | 学生登录 | 第四章 | 待人工截图 |
| 4 | `fig-04-vent-page.png` | 匿名树洞页 | `/vent` | 学生登录 | 第四章 | 待人工截图 |
| 5 | `fig-05-emotion-page.png` | 情绪感知交互页 | `/emotion` | 学生登录 | 第四章 | 待人工截图 |
| 6 | `fig-06-appointments-page.png` | 咨询预约页 | `/appointments` | 学生登录 | 第四章 | 待人工截图 |
| 7 | `fig-07-admin-dashboard.png` | 后台总览页 | `/admin/dashboard` | 后台登录 | 第四章 | 待人工截图 |
| 8 | `fig-08-admin-records.png` | 后台记录页 | `/admin/assessments` 或 `/admin/appointments` | 后台登录 | 第四章 | 待人工截图 |
| 9 | `fig-09-screen-dashboard.png` | 大屏看板页 | `/screen` | 否 | 第四章 | 待人工截图 |

## 3. 图示源文件与导出目标

| 编号 | 源文件 | 导出文件名 | 报告章节 | 当前状态 |
| --- | --- | --- | --- | --- |
| 10 | `docs/assets/system-flow.md` | `fig-10-system-flow.png` | 第三章 | 已生成源码，待导出图片 |
| 11 | `docs/assets/er-diagram.md` | `fig-11-er-diagram.png` | 第四章 | 已生成源码，待导出图片 |
| 12 | `docs/assets/class-tree.md` | `fig-12-class-tree.png` | 第三章 | 已生成源码，待导出图片 |

## 4. 测试附件清单

| 编号 | 建议文件名 | 内容 | 生成方式 | 当前状态 |
| --- | --- | --- | --- | --- |
| T-01 | `tab-01-functional-tests.png` | 功能测试表截图 | 由 `docs/test-report.md` 导出或截图 | 已有表格底稿 |
| T-02 | `tab-02-performance-tests.png` | 性能测试表截图 | 由 `docs/test-report.md` 导出或截图 | 已有实测数据 |
| T-03 | `tab-03-compatibility-tests.png` | 兼容性测试表截图 | 由 `docs/test-report.md` 导出或截图 | 待人工实机验证 |
| T-04 | `tab-04-pytest-result.png` | 自动化测试通过截图 | 运行 `python -m pytest -q` 后截图终端 | 待人工截图 |

## 5. 采集顺序建议
1. 先运行 `python run.py`。
2. 先截学生端 6 张图。
3. 再截后台 2 张图。
4. 最后截大屏 1 张图。
5. 用本目录 3 个 Mermaid 源文件导出结构图。
6. 把 `docs/test-report.md` 中的功能、性能、兼容性表格导出为报告附图或表格。
