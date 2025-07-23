# AI Pop Quiz

AI Pop Quiz 是一个基于人工智能的交互式实时课堂测验系统，旨在增强演讲和教学体验。该项目允许演讲者在演讲过程中根据演讲内容生成实时测验，收集听众反馈，并促进演讲后的讨论与分析。

## 项目概述

AI Pop Quiz 采用前后端分离架构：
- **前端**：基于 Vue 3 构建的响应式 Web 应用
- **后端**：使用 Flask 框架的 Python API 服务
- **实时通信**：使用 WebSocket 实现演讲者与听众之间的即时交互

## 核心功能

### 用户角色系统
- **组织者**：创建和管理演讲活动，查看统计数据和报告
- **演讲者**：上传演讲材料，生成随堂测验，接收实时反馈
- **听众**：参与演讲，回答测验题，提供反馈，参与讨论

### 智能测验生成
- 基于上传的演讲材料（PDF、DOCX、文本）自动生成测验题
- 支持多种文件格式解析和文本提取
- 利用大语言模型生成高质量的选择题

### 实时互动
- 测验问题即时推送给所有听众
- 演讲者可查看实时答题统计
- 听众可提供即时反馈（如"讲得太快"、"内容乏味"等）

### 课后讨论与分析
- 每个测验题目自动生成讨论区
- 完整的个人和整体统计报告
- 演讲表现数据分析

## 技术特点

### 前端（Vue 3）
- 响应式设计，适配多种设备
- 组件化架构，提高代码复用性
- 实时数据更新和动态UI

### 后端（Flask）
- RESTful API 设计
- JWT 认证机制
- SQLAlchemy ORM 数据模型
- Socket.IO 实现实时通信

## 快速开始

### 系统要求
- [Docker](https://docs.docker.com/get-docker/) (19.03.0+)
- [Docker Compose](https://docs.docker.com/compose/install/) (1.27.0+)

### 方法一：一键部署（推荐）

1. 克隆项目
   ```bash
   git clone https://github.com/a-normal-team/summer-project.git
   ```

2. 运行部署脚本
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

3. 访问应用
   - 前端：http://localhost:8080
   - 后端API：http://localhost:5000/api

### 方法二：分别部署前后端

#### 后端部署
1. 进入后端目录
   ```bash
   cd back-flask
   ```

2. 使用Docker Compose启动后端
   ```bash
   docker-compose up -d
   ```

#### 前端部署
1. 进入前端目录
   ```bash
   cd front-vue/vue-project
   ```

2. 使用Docker Compose启动前端
   ```bash
   docker-compose up -d
   ```

### 停止服务
```bash
docker-compose down
```

### 环境变量配置
项目根目录下的`.env`文件包含了应用所需的环境变量配置。部署脚本会自动创建默认配置，您也可以根据需要自行修改：

```
# API服务配置
SECRET_KEY=your_secret_key_here
JWT_SECRET_KEY=your_jwt_secret_key_here

# 前端服务配置
VITE_API_BASE_URL=http://localhost:5000/api
```

### 常见问题
1. **端口冲突**: 如果5000或8080端口已被占用，请修改`docker-compose.yml`中的端口映射。
2. **数据库**: 项目默认使用SQLite数据库，存储在`back-flask/app/site.db`文件中。
3. **日志查看**: 使用`docker-compose logs -f [service]`命令查看服务日志。

## 演示流程

1. **准备阶段**：
   - 组织者创建演讲并分配演讲者
   - 演讲者上传演讲材料
   - 听众加入演讲

2. **演讲中**：
   - 演讲者生成随堂测验
   - 听众接收并回答测验题
   - 演讲者实时查看答题情况
   - 听众提供即时反馈

3. **演讲后**：
   - 听众查看个人表现报告
   - 参与题目讨论
   - 演讲者查看详细统计和反馈
   - 组织者分析整体表现

## 项目结构
- **back-flask/**: 后端 Flask 应用
  - **app/**: 应用核心代码
    - **models.py**: 数据模型定义
    - **utils.py**: 工具函数
    - **routes/**: API 路由
  - **API_Documentation.md**: API 文档

- **front-vue/**: 前端 Vue 应用
  - **vue-project/**: Vue 项目
    - **src/**: 源代码
      - **components/**: Vue 组件
      - **services/**: API 服务
      - **router/**: 路由配置

## 作者
南京理工大学 2025年暑期项目 
