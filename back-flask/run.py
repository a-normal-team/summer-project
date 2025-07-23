from dotenv import load_dotenv
load_dotenv() # 加载 .env 文件中的环境变量

import os # Add this import
from app import create_app, socketio # Import socketio

# 只在开发环境中重置数据库
if os.environ.get('FLASK_ENV') == 'development' and os.path.exists('site.db'):
    os.remove('site.db')
    print("Removed existing site.db for a clean start.")

app, socketio = create_app() # Get both app and socketio

if __name__ == '__main__':
    socketio.run(app, debug=True) # Run with socketio
