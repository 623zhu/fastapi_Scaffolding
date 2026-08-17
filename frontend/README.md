# Frontend

Vue 3 + TypeScript 前端。开发服务器会把 `/api` 代理到 `VITE_API_PROXY_TARGET`，默认值为 `http://127.0.0.1:8001`。

```bash
npm install
npm run dev
```

检查命令：

```bash
npm run lint
npm run type-check
npm run test:unit -- --run
npm run build
npm run test:e2e
```

端到端测试默认访问 `http://127.0.0.1:8080`，运行前需先在项目根目录启动 Docker Compose。可通过 `PLAYWRIGHT_BASE_URL` 改为其他部署地址。
