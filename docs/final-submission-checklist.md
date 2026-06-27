# 最终提交包检查清单

## 1. 用途
- 在最终交老师前，按一次性检查方式确认源码、文档、SQL 和报告是否齐套。
- 本文件是内部过程清单，不直接提交给老师。

## 2. 最终提交目录命名
- 根目录命名：`班级-姓名-学号`

## 2.1 当前状态清单（`2026-06-27`）
- 统一代码分支：已在 `feat/backend-core` 集成学生端、后台端、大屏端优化页面。
- 数据库运行边界：已改为 MySQL-only，非测试环境禁止使用 SQLite 或其他数据库。
- 自动化测试：已执行 `python -m pytest -q`，当前为 `40 passed`。
- 已补统一版截图：`fig-01`、`fig-07`、`fig-09`。
- 已补结构图：`fig-10`、`fig-11`、`fig-12`。
- 仍待补最终资产：`fig-02` 到 `fig-06`、`fig-08`、兼容性实机记录、正式 Word 报告。

## 3. 必须包含

### 3.1 源码工程
- `app/`
- `templates/`
- `static/`
- `tests/`
- `run.py`
- `requirements.txt`
- `.env.example`
- `pytest.ini`

### 3.2 数据库脚本
- `sql/schema.sql`
- `sql/seed.sql`

### 3.3 说明文档
- `docs/deployment-guide.md`
- `docs/database-design.md`

### 3.4 正式课程报告
- 一个按老师模板排版完成的 `Word` 文件
- 内容来源应以 `docs/course-report-draft.md`、`docs/test-report.md` 和 `docs/assets/` 为准

## 4. 不应包含
- `.git/`
- `.pytest_cache/`
- `__pycache__/`
- 老师发下来的原始要求文档
- `docs/superpowers/`
- `docs/document-control.md`
- `docs/requirements-audit.md`
- `docs/final-submission-checklist.md`
- 仅用于仓库管理的底稿文件

## 5. 报告插图检查
- `fig-01`、`fig-07`、`fig-09` 已采集
- `fig-02` 到 `fig-06`、`fig-08` 待补
- `fig-10-system-flow.png` 已导出
- `fig-11-er-diagram.png` 已导出
- `fig-12-class-tree.png` 已导出
- 功能、性能、兼容性测试表待插入正式 Word 报告

## 6. 测试证据检查
- 自动化测试命令 `python -m pytest -q` 已重新执行
- 自动化测试文本证据已留档到 `docs/assets/test-evidence/pytest-full-2026-06-27.txt`
- 自动化测试截图仍待人工补采
- 兼容性测试尚未在手机 Chrome、PC Chrome、PC Edge 和 `1920x1080` 大屏实机验证
- 人工功能测试截图已部分采集，详见 `docs/assets/capture-checklist.md`

## 7. 内容一致性检查
- 报告中的路由、模块名、数据表名与源码一致
- 报告中的数据库说明与 `sql/schema.sql` 一致
- 报告中的测试结果与 `docs/test-report.md` 一致
- 报告中未写入未实现功能

## 8. 提交前最后一步
1. 复制出最终提交目录。
2. 删除不提交的内部过程文件。
3. 把 Markdown 底稿内容转写到 Word 模板。
4. 再次核对截止时间：`第 18 周周三（2026 年 7 月 1 日 24:00 前）`。
