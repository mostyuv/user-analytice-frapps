# User Analytics Dashboard

基于 Frappe 框架开发的用户增长数据分析平台，通过数据大屏直观展示用户增长趋势与分布情况。

## 功能特性

- KPI 指标卡片（活跃用户、新增开通、用户流失、收入）
- 用户增长趋势折线图（开通 vs 流失）
- 地区分布饼图、套餐分布环形图、渠道贡献条形图
- 最近事件实时滚动
- CSV 数据导出
- 全屏展示模式
- 响应式布局，适配各种屏幕尺寸

## 技术栈

| 组件 | 技术 |
|------|------|
| 后端框架 | Frappe v16.26.2 |
| ERP 系统 | ERPNext v16.26.2 |
| 数据库 | MariaDB 11.8 |
| 缓存 | Redis 6.2 |
| 前端图表 | Chart.js 4.4.0 |
| 截图 | html2canvas 1.4.1 |
| 容器化 | Docker Compose |

## 快速部署

### 前置要求

- Docker Desktop（Windows / Mac）或 Docker Engine（Linux）
- 至少 4GB 可用内存

### 部署步骤

```bash
# 1. 克隆项目
git clone https://github.com/mostyuv/user-analytice-frapps.git
cd user-analytice-frapps

# 2. 配置环境变量
cp frappe_docker/.env.example frappe_docker/.env
# 编辑 .env，修改以下密码：
#   DB_PASSWORD=你的数据库密码
#   MYSQL_ROOT_PASSWORD=你的MySQL root密码
#   MARIADB_ROOT_PASSWORD=你的MariaDB root密码
#   ADMIN_PASSWORD=Frappe管理员密码

# 3. 启动所有服务
cd frappe_docker
docker-compose up -d

# 4. 等待初始化完成（首次启动约 3-5 分钟）
# 查看日志确认初始化完成
docker-compose logs -f create-site
# 看到 "site created" 相关输出后 Ctrl+C 退出

# 5. 访问
# 数据大屏：http://localhost:8080/user-growth-dashboard
# 后台管理：http://localhost:8080/login
```

## 环境变量说明

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `DB_PASSWORD` | 数据库密码 | - |
| `MYSQL_ROOT_PASSWORD` | MySQL root 密码 | - |
| `MARIADB_ROOT_PASSWORD` | MariaDB root 密码 | - |
| `ADMIN_PASSWORD` | Frappe 管理员密码 | - |
| `HTTP_PUBLISH_PORT` | Web 服务端口 | 8080 |
| `GUNICORN_WORKERS` | Gunicorn 工作进程数 | 2 |
| `GUNICORN_THREADS` | Gunicorn 线程数 | 4 |

## 项目结构

```
.
├── frappe_app/
│   └── user_analytics/                # 自定义 Frappe App
│       ├── doctypes/
│       │   └── User_Service_Event/    # 用户服务事件 DocType
│       ├── pages/
│       │   └── user_growth_dashboard.py  # 数据大屏后端 API
│       ├── reports/
│       │   └── 用户增长数据报表/       # 报表
│       ├── www/
│       │   └── user-growth-dashboard.html  # 数据大屏前端页面
│       ├── hooks.py                   # Frappe 钩子配置
│       └── install.py                 # 安装脚本（含演示数据）
│
├── frappe_docker/                     # Docker 部署配置
│   ├── docker-compose.yml             # 容器编排
│   ├── .env.example                   # 环境变量模板
│   └── ...
│
└── .gitignore
```

## 访问地址

| 页面 | URL |
|------|-----|
| 数据大屏 | http://localhost:8080/user-growth-dashboard |
| 后台登录 | http://localhost:8080/login |
| 管理员账号 | `Administrator` / 见 `.env` 中 `ADMIN_PASSWORD` |

## License

MIT
