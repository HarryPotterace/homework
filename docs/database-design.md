# 数据库设计说明

## 1. 文档用途
- 说明系统数据库表结构、字段含义、关系约束和 ER 图。

## 2. 必含内容
- `users`
- `admins`
- `scales`
- `scale_questions`
- `assessment_records`
- `vent_posts`
- `behavior_logs`
- `counselors_schedule`
- `appointments`

## 3. 建议正文结构
- 3.1 数据库设计目标
- 3.2 核心实体说明
- 3.3 表结构与字段说明
- 3.4 主外键与关联关系
- 3.5 ER 图位置与说明
- 3.6 脱敏字段处理说明

## 4. 当前状态
- 骨架已创建，`sql/schema.sql` 与 `sql/seed.sql` 已建立，待回填字段细节和 ER 图。
