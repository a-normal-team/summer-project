# 演示Web项目

这是一个简单的全栈Web应用程序演示，包含使用Express构建的后端和使用React构建的前端。

## 项目结构

```
demo-web-project
├── backend
│   ├── src
│   │   ├── controllers
│   │   │   └── api.js
│   │   ├── routes
│   │   │   └── index.js
│   │   └── server.js
│   ├── package.json
│   └── .env
├── frontend
│   ├── public
│   │   ├── index.html
│   │   └── style.css
│   ├── src
│   │   ├── components
│   │   │   └── App.js
│   │   └── index.js
│   └── package.json
└── .vscode
```

## 环境要求

- Node.js（14版本或更高）
- npm（Node包管理器）

## 开始使用

### 后端

1. 进入后端目录：
   ```
   cd backend
   ```

2. 安装后端依赖：
   ```
   npm install
   ```

3. 在后端目录中创建`.env`文件并指定端口：
   ```
   PORT=5000
   ```

4. 启动后端服务器：
   ```
   npm start
   ```

### 前端

1. 打开新终端并进入前端目录：
   ```
   cd frontend
   ```

2. 安装前端依赖：
   ```
   npm install
   ```

3. 启动前端开发服务器：
   ```
   npm start
   ```

## 访问应用

当两个服务器都运行后，您可以通过在Web浏览器中访问`http://localhost:3000`来使用前端应用。后端API将在`http://localhost:5000/api`可用。

## 总结

该项目作为构建全栈Web应用程序的基本模板。您可以通过添加更多功能和特性来扩展它。