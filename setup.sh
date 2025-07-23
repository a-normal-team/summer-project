#!/bin/bash

# AI Pop Quiz 一键部署脚本

# 显示欢迎信息
echo "================================================"
echo "      欢迎使用 AI Pop Quiz 一键部署脚本"
echo "================================================"
echo "该脚本将帮助你部署AI Pop Quiz的前后端服务"
echo ""

# 检查是否安装了Docker和Docker Compose
if ! command -v docker &> /dev/null; then
    echo "错误: Docker未安装。请先安装Docker: https://docs.docker.com/get-docker/"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "错误: Docker Compose未安装。请先安装Docker Compose: https://docs.docker.com/compose/install/"
    exit 1
fi

echo "检测到Docker和Docker Compose已安装..."
echo ""

# 创建.env文件
echo "创建环境配置文件..."
cat > .env << EOL
# API服务配置
SECRET_KEY=deb9b858c62af5349ae342e94a7ab2f5
JWT_SECRET_KEY=bda0032f56b9c2206780343cc7d643502f1be5f95b7eae739471d58527f74a8b

# 前端服务配置
VITE_API_BASE_URL=http://localhost:5000/api
EOL
echo "环境配置文件创建完成."
echo ""

# 创建主docker-compose.yml文件
echo "创建主docker-compose.yml文件..."
cat > docker-compose.yml << EOL
version: '3'

services:
  backend:
    build: ./back-flask
    ports:
      - "5000:5000"
    volumes:
      - ./back-flask/app/site.db:/app/app/site.db
    environment:
      - SECRET_KEY=\${SECRET_KEY}
      - JWT_SECRET_KEY=\${JWT_SECRET_KEY}
    restart: unless-stopped

  frontend:
    build: ./front-vue/vue-project
    ports:
      - "8080:80"
    environment:
      - VITE_API_BASE_URL=\${VITE_API_BASE_URL}
    depends_on:
      - backend
EOL
echo "主docker-compose.yml文件创建完成."
echo ""

# 启动服务
echo "开始构建和启动服务..."
docker-compose up -d --build

# 检查服务是否成功启动
if [ $? -eq 0 ]; then
    echo ""
    echo "================================================"
    echo "    AI Pop Quiz 已成功部署!"
    echo "================================================"
    echo ""
    echo "前端服务访问地址: http://localhost:8080"
    echo "后端API服务访问地址: http://localhost:5000/api"
    echo ""
    echo "使用以下命令查看服务日志:"
    echo "  前端日志: docker-compose logs -f frontend"
    echo "  后端日志: docker-compose logs -f backend"
    echo ""
    echo "使用以下命令停止服务:"
    echo "  docker-compose down"
    echo ""
    echo "祝您使用愉快!"
else
    echo ""
    echo "================================================"
    echo "    AI Pop Quiz 部署失败，请查看错误信息"
    echo "================================================"
fi
