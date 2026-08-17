# FastAPI Vue Starter

一个可直接上传到 GitHub 并重复使用的全栈项目脚手架。生产编排包含 Vue 3 + TypeScript、FastAPI、MySQL、Redis 和 Nginx；数据库迁移由 Alembic 在后端启动前自动执行。

## 一键启动

前置条件：Docker Desktop 已启动，并支持 Docker Compose v2。

```bash
cp .env.example .env
docker compose up --build -d
```

启动完成后可访问：

- Web 注册页：http://127.0.0.1:8080
- FastAPI 文档：http://127.0.0.1:8001/docs
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

## 目录

```text
.
|-- backend/              FastAPI、SQLAlchemy、Alembic、测试
|-- frontend/             Vue 3、TypeScript、Vite、Vitest、Playwright
|-- deploy/nginx/         静态资源服务与 API 反向代理
|-- .github/workflows/    GitHub Actions
|-- compose.yaml          一键生产式启动
|-- compose.dev.yaml      本地热更新覆盖
`-- .env.example          项目集中配置模板
```

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
