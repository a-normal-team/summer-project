"""
数据库迁移脚本 - 添加 Feedback 表的 content 字段
"""
import sqlite3
import os

def migrate():
    # 获取数据库路径
    db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'app/site.db')
    
    # 确保数据库文件存在
    if not os.path.exists(db_path):
        print(f"数据库文件不存在: {db_path}")
        return False
    
    try:
        # 连接到数据库
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 检查 feedback 表是否存在
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='feedback';")
        if not cursor.fetchone():
            print("feedback 表不存在，无需迁移")
            return False
        
        # 检查 content 字段是否已存在
        cursor.execute("PRAGMA table_info(feedback);")
        columns = cursor.fetchall()
        column_names = [column[1] for column in columns]
        
        if 'content' in column_names:
            print("content 字段已存在，无需迁移")
            return True
        
        # 添加 content 字段
        cursor.execute("ALTER TABLE feedback ADD COLUMN content TEXT;")
        
        # 提交更改
        conn.commit()
        print("成功添加 content 字段到 feedback 表")
        
        return True
    
    except sqlite3.Error as e:
        print(f"数据库迁移错误: {e}")
        return False
    
    finally:
        # 关闭连接
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    migrate()
