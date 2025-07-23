# AI Pop Quiz 前端 Docker 指南

本文档提供了如何使用Docker构建和运行AI Pop Quiz前端应用的说明。

## 前提条件

确保您的系统上已安装以下软件：

- Docker (20.10+)
- Docker Compose (v2+)

## 构建和运行Docker镜像

### 使用Docker Compose（推荐）

1. 在项目根目录中，运行：

```bash
docker-compose up -d
```

这将构建前端应用并在后台运行容器。应用将在 http://localhost:8080 可访问。

### 仅使用Docker

1. 构建镜像：

```bash
docker build -t ai-pop-quiz-frontend .
```

2. 运行容器：

```bash
docker run -d -p 8080:80 -e VITE_API_BASE_URL=http://your-api-url/api ai-pop-quiz-frontend
```

## 环境变量

您可以通过环境变量自定义应用的行为：

- `VITE_API_BASE_URL`: API服务器的基础URL

## 自定义Nginx配置

如果需要自定义Nginx配置，您可以编辑项目根目录中的`nginx.conf`文件。修改后需要重新构建镜像。

## 生产部署注意事项

对于生产环境，请确保：

1. 更新`.env.production`中的环境变量，特别是API URL
2. 配置适当的CORS设置
3. 考虑使用HTTPS
4. 根据需要配置适当的缓存策略

## 故障排除

### 常见问题

1. **无法连接到API**
   - 检查`VITE_API_BASE_URL`环境变量是否正确设置
   - 确保API服务器正在运行并可从容器访问

2. **页面加载后显示空白**
   - 检查浏览器控制台中的JavaScript错误
   - 验证构建是否正确完成

### 查看容器日志

```bash
docker-compose logs -f frontend
```

或者如果直接使用Docker：

```bash
docker logs -f <容器ID>
```
