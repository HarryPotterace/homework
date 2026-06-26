# 数据库设计说明

## 1. 文档用途
- 说明系统数据库表结构、字段含义、关系约束和 ER 图。
- 本文与 `sql/schema.sql`、`sql/seed.sql` 保持一致，作为最终提交中的“数据库说明”底稿。

## 2. 数据库设计目标
- 支撑学生端、后台端和大屏端的统一业务数据存储。
- 保持结构简单，便于课程作业部署、演示和说明。
- 保证匿名树洞与大屏聚合展示的数据脱敏要求。

## 3. 核心实体
- 学生：`users`
- 后台账号：`admins`
- 量表：`scales`
- 量表题目：`scale_questions`
- 测评记录：`assessment_records`
- 树洞记录：`vent_posts`
- 行为日志：`behavior_logs`
- 咨询师排班：`counselors_schedule`
- 预约记录：`appointments`

## 4. 表结构说明

### 4.1 `users`
用途：存储学生注册信息。

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `id` | `INT` | 主键 |
| `student_no` | `VARCHAR(20)` | 学号，唯一 |
| `name` | `VARCHAR(50)` | 真实姓名 |
| `nickname` | `VARCHAR(50)` | 昵称，页面主要展示字段 |
| `contact` | `VARCHAR(50)` | 联系方式 |
| `password_hash` | `VARCHAR(255)` | 密码哈希 |
| `created_at` | `DATETIME` | 创建时间 |

### 4.2 `admins`
用途：存储咨询师与管理员后台账号。

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `id` | `INT` | 主键 |
| `username` | `VARCHAR(50)` | 后台登录账号，唯一 |
| `name` | `VARCHAR(50)` | 姓名 |
| `role` | `VARCHAR(20)` | 角色，默认 `consultant` |
| `contact` | `VARCHAR(50)` | 联系方式 |
| `password_hash` | `VARCHAR(255)` | 密码哈希 |
| `created_at` | `DATETIME` | 创建时间 |

### 4.3 `scales`
用途：存储量表元数据。

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `id` | `INT` | 主键 |
| `code` | `VARCHAR(20)` | 量表编码，如 `PHQ-9` |
| `name` | `VARCHAR(100)` | 量表名称 |
| `description` | `TEXT` | 量表简介 |

### 4.4 `scale_questions`
用途：存储量表题目。

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `id` | `INT` | 主键 |
| `scale_code` | `VARCHAR(20)` | 关联 `scales.code` |
| `question_order` | `INT` | 题目序号 |
| `content` | `TEXT` | 题目内容 |

### 4.5 `assessment_records`
用途：存储学生测评结果。

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `id` | `INT` | 主键 |
| `user_id` | `INT` | 关联学生 |
| `scale_code` | `VARCHAR(20)` | 量表编码 |
| `scale_name` | `VARCHAR(100)` | 量表名称快照 |
| `score` | `INT` | 得分 |
| `result_level` | `VARCHAR(50)` | 结果等级 |
| `advice` | `TEXT` | 系统建议 |
| `created_at` | `DATETIME` | 提交时间 |

### 4.6 `vent_posts`
用途：存储匿名树洞内容及情绪标签。

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `id` | `INT` | 主键 |
| `user_id` | `INT` | 可空，关联学生 |
| `title` | `VARCHAR(100)` | 树洞标题 |
| `content` | `TEXT` | 树洞正文 |
| `emotion` | `VARCHAR(20)` | 文本情绪标签 |
| `risk_level` | `VARCHAR(20)` | 风险等级 |
| `is_anonymous` | `BOOLEAN` | 是否匿名 |
| `created_at` | `DATETIME` | 发布时间 |

### 4.7 `behavior_logs`
用途：存储情绪感知页采集到的交互行为特征与推断结果。

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `id` | `INT` | 主键 |
| `user_id` | `INT` | 可空，关联学生 |
| `page_name` | `VARCHAR(50)` | 页面标识 |
| `mouse_speed` | `FLOAT` | 鼠标速度指标 |
| `click_count` | `INT` | 点击频次 |
| `pause_count` | `INT` | 输入停顿次数 |
| `emotion` | `VARCHAR(20)` | 行为推断情绪 |
| `ui_mode` | `VARCHAR(20)` | 界面模式 |
| `created_at` | `DATETIME` | 采集时间 |

### 4.8 `counselors_schedule`
用途：存储咨询师排班。

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `id` | `INT` | 主键 |
| `counselor_name` | `VARCHAR(50)` | 咨询师姓名 |
| `title` | `VARCHAR(50)` | 职称 |
| `schedule_date` | `VARCHAR(20)` | 日期 |
| `slot` | `VARCHAR(50)` | 时段 |
| `is_available` | `BOOLEAN` | 是否可预约 |

### 4.9 `appointments`
用途：存储学生预约记录。

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `id` | `INT` | 主键 |
| `user_id` | `INT` | 关联学生 |
| `schedule_id` | `INT` | 关联排班时段 |
| `status` | `VARCHAR(20)` | 预约状态，默认 `待确认` |
| `note` | `VARCHAR(255)` | 预约备注 |
| `created_at` | `DATETIME` | 预约创建时间 |

## 5. 主外键关系
- `assessment_records.user_id -> users.id`
- `vent_posts.user_id -> users.id`
- `behavior_logs.user_id -> users.id`
- `appointments.user_id -> users.id`
- `appointments.schedule_id -> counselors_schedule.id`
- `scale_questions.scale_code -> scales.code`

关系说明：
- 一个学生可以对应多条测评记录、树洞记录、行为日志和预约记录。
- 一个排班时段可被预约记录引用，用 `is_available` 控制是否继续开放。
- 一个量表对应多道题目。

## 6. 脱敏处理说明
- 树洞前台页面默认匿名，不显示学号和姓名。
- 大屏页面只读取汇总统计结果，不直接展示 `users.contact`、`users.name`、`users.student_no` 等身份字段。
- 后台页面可见学生学号与昵称，用于咨询师和管理员业务处理，不向大屏端透出。

## 7. ER 图说明
- 正式课程报告需插入本系统 ER 图。
- 图中至少包含：`users`、`assessment_records`、`vent_posts`、`behavior_logs`、`counselors_schedule`、`appointments`、`scales`、`scale_questions`。
- ER 图素材文件建议放入 `docs/assets/fig-11-er-diagram.png`。

## 8. 与 SQL 文件的对应关系
- 建表主来源：`sql/schema.sql`
- 初始化数据主来源：`sql/seed.sql`
- 若表结构发生变化，应先修改 SQL，再回写本文。
