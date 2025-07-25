"""
工具函数包
包含各种辅助功能的工具函数和类
"""

# 导入常用函数，使它们可以通过app.utils直接访问
from .auth import role_required
from .file_processing import extract_text_from_file
