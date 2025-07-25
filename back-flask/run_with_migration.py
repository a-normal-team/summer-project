"""
启动脚本，包含数据库迁移
"""
from dotenv import load_dotenv
load_dotenv()  # 加载 .env 文件中的环境变量

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 确保目录存在
migrations_dir = os.path.join(os.path.dirname(__file__), 'migrations')
if not os.path.exists(migrations_dir):
    os.makedirs(migrations_dir)

# 运行迁移
try:
    from migrations.add_feedback_content import migrate
    migrate_result = migrate()
    if migrate_result:
        print("数据库迁移成功完成")
    else:
        print("数据库迁移未完成，继续启动应用")
except ImportError:
    print("未找到迁移脚本，继续启动应用")
except Exception as e:
    print(f"迁移过程中出现错误: {e}")

# 启动应用
from app import create_app, socketio

app = create_app()  # 获取 app 实例

if __name__ == '__main__':
    print("正在启动带有 WebSocket 支持的应用...")
    socketio.run(
        app, 
        debug=True, 
        allow_unsafe_werkzeug=True,
        host='0.0.0.0',  # 允许从任何IP访问
        port=8080        # 指定端口
    )
