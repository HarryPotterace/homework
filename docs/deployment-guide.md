# 系统部署说明书

## 1. 文档用途
- 说明项目如何在新环境中安装、配置、启动和验证。
- 本文可直接作为最终提交中的“系统配置说明书”底稿。

## 2. 工程概览
- 项目类型：`Flask + Jinja2 + Bootstrap + 自定义 CSS/JS + MySQL` 单体 B/S 应用。
- 启动入口：`run.py`
- 配置文件：`.env`
- 数据库脚本：`sql/schema.sql`、`sql/seed.sql`
- 标准测试命令：`python -m pytest -q`

## 3. 环境依赖

### 3.1 软件版本
- Python：建议 `3.13`
- 数据库：MySQL `8.x`
- 浏览器：
  - 学生端：Chrome 移动端或手机浏览器
  - 后台端：Chrome / Edge
  - 大屏端：Chrome 全屏模式

### 3.2 Python 依赖
项目 `requirements.txt` 当前依赖如下：

```txt
Flask==3.1.1
Flask-SQLAlchemy==3.1.1
PyMySQL==1.1.1
python-dotenv==1.1.1
pytest==8.4.1
```

## 4. 安装步骤

### 4.1 获取工程
在项目目录执行：

```powershell
git clone https://github.com/HarryPotterace/homework.git
cd homework
```

如果直接提交课程作业包，则保留源码目录即可，不需要 `.git/`。

### 4.2 安装依赖

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## 5. 数据库配置

### 5.1 创建数据库
默认数据库名为 `mental_health_system`。`sql/schema.sql` 已包含建库语句，也可手动预先创建：

```sql
CREATE DATABASE mental_health_system
  DEFAULT CHARACTER SET utf8mb4
  DEFAULT COLLATE utf8mb4_unicode_ci;
```

### 5.2 导入 SQL
导入顺序固定：

1. `sql/schema.sql`
2. `sql/seed.sql`

示例命令：

```powershell
mysql -u root -p < sql/schema.sql
mysql -u root -p mental_health_system < sql/seed.sql
```

### 5.3 初始化数据说明
`seed.sql` 会导入：
- 后台演示账号
- `PHQ-9`、`GAD-7` 两类量表
- 量表题目
- 咨询师排班数据

当前可直接登录的后台演示账号：
- `consultant / Admin12345`
- `admin / Admin12345`

学生账号不预置，通过学生端注册页面创建。

## 6. `.env` 配置说明

`.env.example` 当前内容：

```env
SECRET_KEY=change-me
DATABASE_URL=mysql+pymysql://root:password@127.0.0.1:3306/mental_health_system?charset=utf8mb4
```

复制为 `.env` 后按实际环境修改：

### 6.1 `SECRET_KEY`
- 用于 Flask Session 签名。
- 本地演示可自定义任意随机字符串。

### 6.2 `DATABASE_URL`
- 正式 MySQL 连接串。
- 必须显式配置，未配置时应用会直接拒绝启动。
- 运行环境只允许 `mysql+pymysql://...` 格式连接串，不允许退回到其他数据库。

## 7. 启动方式

### 7.1 启动命令

```powershell
python run.py
```

当前 `run.py` 以 `debug=True` 方式启动，默认监听 Flask 开发服务器。

### 7.2 访问入口
- 学生端首页：`/`
- 学生登录：`/login`
- 学生注册：`/register`
- 后台登录：`/admin/login`
- 大屏端：`/screen`

## 8. 本地验证步骤

### 8.1 自动化验证

```powershell
python -m pytest -q
```

当前代码基线测试通过后应输出全部通过结果。

### 8.2 人工验证
建议按以下顺序验收：

1. 注册学生账号并登录。
2. 完成一次 `PHQ-9` 或 `GAD-7` 测评。
3. 发布一条匿名树洞内容。
4. 进入情绪感知页，观察行为采集后的提示变化。
5. 提交一次预约并取消预约。
6. 使用后台账号登录，查看测评、树洞和预约页面。
7. 打开 `/screen`，检查大屏是否只显示脱敏聚合数据。

## 9. 常见问题排查

### 9.1 `pytest` 命令环境不一致
- 本项目正式验证统一使用 `python -m pytest -q`。
- 不建议直接使用系统里的裸 `pytest`，避免命中其它 Python 环境。

### 9.2 MySQL 连接失败
- 检查 `.env` 中 `DATABASE_URL` 是否正确。
- 检查 MySQL 服务是否启动。
- 检查数据库名是否为 `mental_health_system`。

### 9.3 后台账号无法登录
- 检查是否已导入最新 `sql/seed.sql`。
- 若数据库使用旧版本种子数据，重新导入 `seed.sql`。

### 9.4 页面可打开但没有数据
- 检查是否导入 `seed.sql`。
- 检查是否已经在页面执行过测评、树洞或预约操作。

## 10. 提交说明
- 最终提交给老师时，应提交：
  - 完整工程源码
  - 本说明书
  - 数据库 SQL 文件
  - Word 版课程报告
- 最终文件夹命名方式：`班级-姓名-学号`
