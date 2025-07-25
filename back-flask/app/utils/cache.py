"""
[此文件已禁用] - 缓存管理器

根据用户要求，缓存功能已完全移除。
此文件保留在项目中仅供参考，但不再使用。
"""

# 禁用的缓存管理器，提供空实现以避免导入错误
class DisabledCacheManager:
    """禁用的缓存管理器，所有方法都不执行实际操作"""
    
    def __init__(self, *args, **kwargs):
        pass
        
    def init_app(self, app):
        pass
    
    def set(self, key, value, expires_in=300):
        return False
    
    def get(self, key, default=None):
        return default
    
    def delete(self, key):
        return False
    
    def clear(self):
        pass

# 提供一个空实现，以防代码中仍有引用
cache = DisabledCacheManager()
