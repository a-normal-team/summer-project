from dotenv import load_dotenv
load_dotenv() # 加载 .env 文件中的环境变量

import os # Add this import
from app import create_app, socketio # Import socketio

# 只在开发环境中重置数据库
if os.environ.get('FLASK_ENV') == 'development' and os.path.exists('site.db'):
    os.remove('site.db')
    print("Removed existing site.db for a clean start.")

app = create_app() # Get app instance

if __name__ == '__main__':
    # 使用socketio运行应用
    print("正在启动WebSocket服务器...")
    # 从环境变量中获取端口，如果未设置则使用默认端口
    port = int(os.environ.get('PORT', 8080))
    print(f"服务器将在端口 {port} 上启动")
    
    try:
        socketio.run(
            app, 
            debug=True, 
            allow_unsafe_werkzeug=True,
            host='0.0.0.0',  # 允许从任何IP访问
            port=port        # 使用环境变量中的端口
        )
    except OSError as e:
        if "Address already in use" in str(e):
            print("\n错误: 端口已被占用!")
            print(f"端口 {port} 被其他程序占用。请尝试以下解决方法:")
            print("1. 关闭占用该端口的程序")
            print("2. 使用其他端口，通过设置环境变量: export PORT=8080")
            print("3. 在macOS上，尝试关闭系统偏好设置->共享->AirPlay接收器")
            import sys
            sys.exit(1)
        else:
            raise
