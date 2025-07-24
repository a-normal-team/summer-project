<script setup>
import { authState, logout, fetchUserProfile } from './services/auth';
import { computed, onMounted, watch } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute();

// 在组件挂载时获取用户资料
onMounted(async () => {
  console.log('App.vue mounted, authState:', authState);
  if (authState.isAuthenticated && !authState.user) {
    try {
      await fetchUserProfile();
      console.log('App.vue - 用户资料获取成功:', authState.user);
    } catch (error) {
      console.error('App.vue - 获取用户资料失败:', error);
    }
  }
  
  // 设置令牌更新事件监听器
  const handleTokenUpdate = (event) => {
    const { userRole, userId } = event.detail;
    console.log(`[App.vue] 收到令牌更新事件: ${userRole} (${userId})`);
    
    // 获取当前标签页的角色和用户标识符
    const currentRole = localStorage.getItem('currentUserRole');
    const currentUserId = localStorage.getItem('currentUserIdentifier');
    
    // 只有在当前标签页无登录信息或是同一用户同一角色时，才更新用户资料
    if (!currentRole || !currentUserId || (currentRole === userRole && currentUserId === userId)) {
      console.log('[App.vue] 处理令牌更新：获取用户资料');
      // 如果当前没有用户资料，尝试获取
      if (authState.isAuthenticated) {
        fetchUserProfile().catch(error => {
          console.error('[App.vue] 令牌更新后获取用户资料失败:', error);
        });
      }
    } else {
      console.log(`[App.vue] 不处理令牌更新：当前标签页已有不同的用户/角色登录 (${currentRole}/${currentUserId})`);
    }
  };
  
  // 设置退出登录事件监听器
  const handleLogoutEvent = (event) => {
    const { userRole, userId } = event.detail;
    console.log(`[App.vue] 收到退出登录事件: ${userRole} (${userId})`);
    
    // 获取当前标签页的角色和用户标识符
    const currentRole = localStorage.getItem('currentUserRole');
    const currentUserId = localStorage.getItem('currentUserIdentifier');
    
    // 只有在当前标签页是同一个用户在同一个角色下登录时，才处理退出登录事件
    if (!currentRole || !currentUserId || (currentRole === userRole && currentUserId === userId)) {
      console.log('[App.vue] 处理退出登录事件');
    } else {
      console.log(`[App.vue] 不处理退出登录事件：当前标签页已有不同的用户/角色登录 (${currentRole}/${currentUserId})`);
    }
  };
  
  // 添加事件监听器
  window.addEventListener('auth_token_updated', handleTokenUpdate);
  window.addEventListener('auth_logout', handleLogoutEvent);
  
  // 组件卸载时移除事件监听器
  return () => {
    window.removeEventListener('auth_token_updated', handleTokenUpdate);
    window.removeEventListener('auth_logout', handleLogoutEvent);
  };
});

// 监听认证状态变化
watch(() => authState.isAuthenticated, async (isAuthenticated) => {
  console.log('认证状态变化:', isAuthenticated);
  if (isAuthenticated && !authState.user) {
    try {
      await fetchUserProfile();
      console.log('认证状态变化后获取用户资料:', authState.user);
    } catch (error) {
      console.error('认证状态变化后获取用户资料失败:', error);
    }
  }
});

// 计算当前是否在登录页面
const isLoginPage = computed(() => {
  return route.path === '/login';
});

// 处理注销
const handleLogout = () => {
  logout();
};
</script>

<template>
  <!-- 导航栏 -->
  <header v-if="authState.isAuthenticated && !isLoginPage" class="app-header">
    <div class="header-logo">AI Pop Quiz</div>
    
    <div class="user-info" v-if="authState.isAuthenticated">
      <span class="username">{{ authState.user?.username || '用户' }}</span>
      <span class="role-badge" :class="authState.user?.role || 'default'">
        {{ authState.user?.role === 'organizer' ? '组织者' : 
           authState.user?.role === 'speaker' ? '演讲者' : 
           authState.user?.role === 'listener' ? '听众' : 
           '用户' }}
      </span>
      <button @click="handleLogout" class="logout-button">退出登录</button>
    </div>
  </header>

  <!-- 路由内容 -->
  <main :class="{ 'with-header': authState.isAuthenticated && !isLoginPage }">
    <router-view />
  </main>
</template>

<style>
/* 全局样式 */
body {
  margin: 0;
  padding: 0;
  font-family: 'Montserrat', sans-serif;
}

/* 导航栏样式 */
.app-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
  background-color: #4dc189;
  color: white;
  height: 60px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.header-logo {
  font-size: 1.5rem;
  font-weight: bold;
}

.user-info {
  display: flex;
  align-items: center;
}

.username {
  margin-right: 10px;
  font-weight: bold;
}

.role-badge {
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 0.8rem;
  margin-right: 15px;
}

.role-badge.organizer {
  background-color: #ff7043;
}

.role-badge.speaker {
  background-color: #42a5f5;
}

.role-badge.listener {
  background-color: #66bb6a;
}

.role-badge.default {
  background-color: #9e9e9e; /* 默认灰色 */
}

.logout-button {
  border: none;
  background-color: rgba(255, 255, 255, 0.2);
  color: white;
  padding: 5px 10px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: background-color 0.3s;
}

.logout-button:hover {
  background-color: rgba(255, 255, 255, 0.3);
}

/* 主内容区域样式 */
main {
  min-height: 100vh;
}

main.with-header {
  padding-top: 60px;
}
</style>
