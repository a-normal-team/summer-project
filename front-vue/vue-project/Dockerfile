# 构建阶段
FROM node:20-alpine as build-stage

# 设置工作目录
WORKDIR /app

# 复制 package.json 和 pnpm-lock.yaml
COPY package.json pnpm-lock.yaml ./

# 安装 pnpm
RUN npm install -g pnpm

# 安装项目依赖
RUN pnpm install

# 复制项目文件
COPY . .

# 构建项目
RUN pnpm build

# 生产阶段
FROM nginx:stable-alpine as production-stage

# 复制构建结果到Nginx目录
COPY --from=build-stage /app/dist /usr/share/nginx/html

# 复制自定义nginx配置
COPY nginx.conf /etc/nginx/conf.d/default.conf

# 暴露端口
EXPOSE 80

# 启动Nginx
CMD ["nginx", "-g", "daemon off;"]
