# FastAPI Vue Starter

一个可直接上传到 GitHub 并重复使用的全栈项目脚手架。生产编排包含 Vue 3 + TypeScript、FastAPI、MySQL、Redis 和 Nginx；数据库迁移由 Alembic 在后端启动前自动执行。

## 一键启动

前置条件：Docker Desktop 已启动，并支持 Docker Compose v2。

脚手架内置了仅用于本地开发和首次验证的默认配置，新克隆后可以直接启动：

```bash
docker compose up --build -d
```

正式项目应先复制配置模板并修改数据库、Redis 密码。PowerShell 使用 `Copy-Item .env.example .env`，Linux/macOS 使用 `cp .env.example .env`。

启动完成后可访问：

- Web 注册页：http://127.0.0.1:8080
- FastAPI 文档：http://127.0.0.1:8001/api/docs
- 就绪检查：http://127.0.0.1:8080/api/v1/health/ready

查看状态和日志：

```bash
docker compose ps
docker compose logs -f
```

停止服务不会删除数据库数据：

```bash
docker compose down
```

## 新项目改名

复制仓库后，优先修改 `.env` 中的这些值：

```dotenv
COMPOSE_PROJECT_NAME=my-project
APP_NAME=My Project
MYSQL_DATABASE=my_project
MYSQL_USER=my_project
MYSQL_PASSWORD=replace-me
MYSQL_ROOT_PASSWORD=replace-root-password
REDIS_PASSWORD=replace-redis-password
```

`COMPOSE_PROJECT_NAME` 控制容器网络和 named volume 的前缀，`APP_NAME` 控制后端名称及前端标题，`MYSQL_DATABASE` 控制首次初始化的数据库名。新克隆的项目可以直接修改；如果 MySQL volume 已经生成，修改数据库名不会自动迁移旧数据。只有确认不需要现有数据时，才使用 `docker compose down -v` 后重新初始化。

## 开发模式

开发覆盖文件会挂载源码并启用 FastAPI、Vite 热更新：

```bash
docker compose -f compose.yaml -f compose.dev.yaml up --build
```

开发页面默认位于 http://127.0.0.1:5173，后端仍位于 http://127.0.0.1:8001。

## 目录结构

```text
.
|-- backend/                              FastAPI 后端
|   |-- app/
|   |   |-- api/                          HTTP 接口层
|   |   |   |-- deps.py                   数据库、Redis 依赖注入
|   |   |   |-- router.py                 API 总路由入口
|   |   |   `-- v1/
|   |   |       |-- router.py             v1 路由聚合
|   |   |       `-- routes/
|   |   |           |-- health.py         存活与就绪检查接口
|   |   |           `-- users.py          用户注册接口
|   |   |-- core/                         跨业务核心能力
|   |   |   |-- config.py                 环境变量读取与配置模型
|   |   |   `-- security.py               Argon2 密码哈希与校验
|   |   |-- db/                           基础设施连接
|   |   |   |-- base.py                   SQLAlchemy 模型基类
|   |   |   |-- session.py                异步 MySQL 引擎和会话工厂
|   |   |   `-- redis.py                  异步 Redis 客户端及关闭逻辑
|   |   |-- models/
|   |   |   `-- user.py                   users 表 ORM 模型
|   |   |-- repositories/
|   |   |   `-- user.py                   用户数据查询与写入
|   |   |-- schemas/
|   |   |   `-- user.py                   注册请求和用户响应模型
|   |   |-- services/
|   |   |   `-- user.py                   用户注册业务逻辑
|   |   `-- main.py                       FastAPI 应用工厂与生命周期
|   |-- alembic/
|   |   |-- versions/
|   |   |   `-- 0001_create_users_table.py 首张用户表迁移
|   |   |-- env.py                        Alembic 运行环境
|   |   `-- script.py.mako                新迁移文件模板
|   |-- tests/
|   |   |-- conftest.py                   测试夹具与依赖覆盖
|   |   |-- test_health.py                健康检查测试
|   |   |-- test_security.py              密码安全测试
|   |   `-- test_user_schema.py           用户模型校验测试
|   |-- alembic.ini                       Alembic 主配置
|   |-- Dockerfile                        后端生产、开发镜像阶段
|   `-- pyproject.toml                     Python 依赖及测试、Ruff 配置
|-- frontend/                              Vue 3 + TypeScript 前端
|   |-- src/
|   |   |-- api/
|   |   |   |-- client.ts                 fetch 封装与统一 API 错误
|   |   |   `-- users.ts                  用户注册请求
|   |   |-- assets/
|   |   |   |-- base.css                  CSS 变量与基础样式
|   |   |   `-- main.css                  全局样式入口
|   |   |-- layouts/                      预留公共布局目录
|   |   |-- router/
|   |   |   `-- index.ts                  Vue Router 路由表
|   |   |-- types/
|   |   |   `-- user.ts                   用户请求、响应类型
|   |   |-- views/
|   |   |   |-- RegisterView.vue          用户注册页面
|   |   |   `-- __tests__/
|   |   |       `-- RegisterView.spec.ts  Vitest 组件测试
|   |   |-- App.vue                       根组件
|   |   `-- main.ts                       Vue、Pinia、Router 初始化
|   |-- e2e/
|   |   `-- register.spec.ts              Playwright 桌面、移动端测试
|   |-- public/
|   |   `-- favicon.ico                   公共静态资源
|   |-- Dockerfile                        Node 构建与 Nginx 运行镜像
|   |-- package.json                      前端依赖和 npm 命令
|   |-- package-lock.json                 可复现依赖锁文件
|   |-- vite.config.ts                    Vite 和开发 API 代理
|   |-- vitest.config.ts                  单元测试配置
|   `-- playwright.config.ts              端到端测试配置
|-- deploy/
|   `-- nginx/
|       `-- default.conf                  SPA 托管、/api 反向代理
|-- .github/
|   `-- workflows/
|       `-- ci.yml                        后端、前端、Compose CI 检查
|-- docs/                                 预留项目文档目录
|-- scripts/                              预留运维和自动化脚本目录
|-- compose.yaml                          完整生产式服务编排
|-- compose.dev.yaml                      前后端热更新覆盖配置
|-- .env.example                          项目名称、端口、密码配置模板
|-- .dockerignore                         Docker 构建上下文排除规则
|-- .gitignore                            Git 忽略规则
`-- README.md                             项目使用说明
```

目录树省略了 Python 包标识文件 `__init__.py`、编辑器配置和各工具的细分配置文件。`frontend/node_modules/`、`frontend/dist/`、测试报告、缓存以及本地 `.env` 都由工具生成或包含本机配置，不会提交到 GitHub。

### 后端分层

一次用户注册请求的调用方向如下：

```text
Nginx -> FastAPI route -> service -> repository -> SQLAlchemy -> MySQL
                         |
                         `-> security（密码哈希）
```

- `routes` 只处理 HTTP 输入、依赖注入和响应状态码。
- `services` 负责业务规则，例如检查用户名或邮箱是否重复、生成密码哈希。
- `repositories` 封装数据库查询和写入，避免业务代码直接拼接查询。
- `models` 描述数据库表结构，`schemas` 描述 API 输入输出，两者职责不同。
- `deps.py` 是 FastAPI 依赖注入入口，目前提供异步数据库会话和 Redis 客户端。

### 前端分层

- `views` 组织页面及交互，当前提供完整用户注册流程。
- `api` 负责 HTTP 请求，页面无需直接处理 `fetch` 和错误响应解析。
- `types` 集中维护与后端接口对应的 TypeScript 类型。
- `router` 管理页面地址，未知路径会回到注册页。
- `e2e` 验证部署后的 Nginx 入口，包含桌面和移动端视口。

### 容器启动顺序

`compose.yaml` 通过 healthcheck 和依赖条件控制启动顺序：

```text
MySQL healthy -> Alembic migrate completed -> FastAPI healthy -> Nginx/Vue
Redis healthy -------------------------------> FastAPI
```

MySQL 和 Redis 数据保存在 named volumes 中；执行 `docker compose down` 会保留数据，执行 `docker compose down -v` 会永久删除数据。

## 常用验证

```bash
cd backend
ruff check .
pytest

cd ../frontend
npm run lint
npm run type-check
npm run test:unit -- --run
npm run build
```
