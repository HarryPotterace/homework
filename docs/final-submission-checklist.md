# 最终提交包检查清单

## 1. 用途
- 在最终交老师前，按一次性检查方式确认源码、文档、SQL 和报告是否齐套。
- 本文件是内部过程清单，不直接提交给老师。

## 2. 最终提交目录命名
- 根目录命名：`班级-姓名-学号`

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
- `fig-01` 到 `fig-09` 页面截图齐全
- `fig-10-system-flow.png` 已由 `docs/assets/system-flow.md` 导出
- `fig-11-er-diagram.png` 已由 `docs/assets/er-diagram.md` 导出
- `fig-12-class-tree.png` 已由 `docs/assets/class-tree.md` 导出
- 功能、性能、兼容性测试表已插入报告

## 6. 测试证据检查
- 自动化测试命令 `python -m pytest -q` 已重新执行
- 自动化测试截图已保存
- 兼容性测试已在手机 Chrome、PC Chrome、PC Edge 和 `1920x1080` 大屏实机验证
- 人工功能测试截图已按 `docs/assets/capture-checklist.md` 采集

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
