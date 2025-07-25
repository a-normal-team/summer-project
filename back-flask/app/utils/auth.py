"""
授权相关的工具函数
包括角色检查、权限验证等功能
"""

from functools import wraps
from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import User

def role_required(role_name):
    """
    装饰器，用于检查用户是否具有特定角色
    :param role_name: 需要的角色名称
    :return: 装饰器函数
    """
    def wrapper(fn):
        @wraps(fn) # 保留原始函数的元数据
        @jwt_required()
        def decorator(*args, **kwargs):
            current_user_id = get_jwt_identity()
            user = User.query.get(current_user_id)
            if user and user.role.name == role_name:
                return fn(*args, **kwargs)
            return jsonify({"msg": f"'{role_name}' role required"}), 403
        return decorator
    return wrapper
