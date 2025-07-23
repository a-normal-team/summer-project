FROM python:3.10-slim

WORKDIR /app

# 复制项目文件
COPY . .

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt

# 初始化数据库
RUN python initialize_db.py

# 暴露端口（默认Flask使用5000端口）
EXPOSE 5000

# 使用gunicorn作为生产环境的WSGI服务器
# 使用eventlet作为socketio工作器
CMD ["gunicorn", "--worker-class", "eventlet", "-w", "1", "--bind", "0.0.0.0:5000", "run:app"]
