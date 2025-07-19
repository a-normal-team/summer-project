from dotenv import load_dotenv
load_dotenv() # 加载 .env 文件中的环境变量

from app import create_app, socketio # Import socketio

app, socketio = create_app() # Get both app and socketio

if __name__ == '__main__':
    socketio.run(app, debug=True) # Run with socketio
