import './assets/main.css';
import './assets/global.css';

import { createApp } from 'vue';
import App from './App.vue';
import router from './router'; // 导入路由
import { checkAuth, authState, navigateToDashboard } from './services/auth'; // 导入认证服务
import { AUTH_CONFIG } from './config'; // 导入配置

// 添加路由守卫
router.beforeEach(async (to, from, next) => {
  // 如果是访问根路径，直接重定向到登录页面
  if (to.path === '/') {
    next('/login');
    return;
  }

  // 需要认证的路由
  const authRequired = to.path.includes('/dashboard');
  
  // 如果认证状态未知，则进行检查
  if (authState.token && !authState.user) {
    await checkAuth();
  }
  
  if (authRequired && !authState.isAuthenticated) {
    next('/login');
  } else if (to.path === '/login' && authState.isAuthenticated) {
    // 如果用户已认证且尝试访问登录页，重定向到相应的仪表板
    navigateToDashboard();
  } else {
    next();
  }
});

// 添加全局事件监听器，以便在所有页面之间同步令牌更新
window.addEventListener('auth_token_updated', (event) => {
  // 接收到令牌更新事件
  const { tokenKey, token, userRole, userId, sessionId: eventSessionId } = event.detail;
  
  console.log(`[主应用] 收到令牌更新事件: ${userRole} (${userId})`);
  
  // 获取当前标签页会话ID
  const currentSessionId = sessionStorage.getItem('browserTabSessionId');
  
  // 如果是当前会话发出的事件，或者当前标签页没有会话ID，则更新localStorage
  if (eventSessionId === currentSessionId || !currentSessionId) {
    console.log('[主应用] 更新localStorage中的令牌信息');
    
    // 更新localStorage中的当前令牌信息（为了兼容性和跨标签页共享）
    localStorage.setItem('currentUserTokenKey', tokenKey);
    localStorage.setItem('currentUserRole', userRole);
    localStorage.setItem('currentUserIdentifier', userId);
    
    // 更新令牌
    localStorage.setItem(tokenKey, token);
    
    // 同时更新角色特定的令牌和通用令牌（以保持兼容性）
    let roleTokenKey = AUTH_CONFIG.TOKEN_KEY; // 默认令牌键
    
    if (userRole === 'speaker') {
      roleTokenKey = AUTH_CONFIG.SPEAKER_TOKEN_KEY;
    } else if (userRole === 'listener') {
      roleTokenKey = AUTH_CONFIG.LISTENER_TOKEN_KEY;
    } else if (userRole === 'organizer') {
      roleTokenKey = AUTH_CONFIG.ORGANIZER_TOKEN_KEY;
    }
    
    localStorage.setItem(roleTokenKey, token); 
    localStorage.setItem(AUTH_CONFIG.TOKEN_KEY, token);
    
    // 如果是当前会话，同时也更新会话存储和认证状态
    if (eventSessionId === currentSessionId) {
      // 更新会话存储
      sessionStorage.setItem('sessionUserRole', userRole);
      sessionStorage.setItem('sessionUserIdentifier', userId);
      sessionStorage.setItem('sessionTokenKey', tokenKey);
      sessionStorage.setItem('sessionToken', token);
      
      // 更新认证状态
      authState.token = token;
      authState.isAuthenticated = true;
      
      console.log('[主应用] 会话令牌状态已同步');
    }
  }
});

// 添加退出登录事件监听器
window.addEventListener('auth_logout', (event) => {
  // 接收到退出登录事件
  const { userRole, userId, tokenKey, sessionId: eventSessionId } = event.detail;
  console.log(`[主应用] 收到退出登录事件: ${userRole} (${userId})`);
  
  // 获取当前标签页会话ID和存储的会话信息
  const currentSessionId = sessionStorage.getItem('browserTabSessionId');
  const sessionUserRole = sessionStorage.getItem('sessionUserRole');
  const sessionUserId = sessionStorage.getItem('sessionUserIdentifier');
  
  // 如果是当前会话发出的事件，清除localStorage中的信息（供其他标签页参考）
  if (eventSessionId === currentSessionId) {
    console.log('[主应用] 清除localStorage中的认证信息');
    
    // 如果有当前用户特定的令牌，清除它
    if (tokenKey) {
      localStorage.removeItem(tokenKey);
    }
    
    // 清除所有角色的令牌存储
    localStorage.removeItem(AUTH_CONFIG.TOKEN_KEY);
    localStorage.removeItem(AUTH_CONFIG.SPEAKER_TOKEN_KEY);
    localStorage.removeItem(AUTH_CONFIG.LISTENER_TOKEN_KEY);
    localStorage.removeItem(AUTH_CONFIG.ORGANIZER_TOKEN_KEY);
    
    // 清除其他存储的用户信息
    localStorage.removeItem('userId');
    localStorage.removeItem('currentUserRole');
    localStorage.removeItem('currentUserIdentifier');
    localStorage.removeItem('currentUserTokenKey');
    localStorage.removeItem('username');
  }
  
  // 只有在当前会话中，或者如果当前标签页登录的是同一个用户同一个角色时，才清除会话存储
  if (eventSessionId === currentSessionId || 
      (sessionUserRole === userRole && sessionUserId === userId)) {
    console.log('[主应用] 清除会话存储中的认证信息');
    
    // 清除会话存储中的认证信息
    sessionStorage.removeItem('sessionUserRole');
    sessionStorage.removeItem('sessionUserIdentifier');
    sessionStorage.removeItem('sessionTokenKey');
    sessionStorage.removeItem('sessionToken');
    
    // 更新认证状态
    authState.token = null;
    authState.user = null;
    authState.isAuthenticated = false;
    
    // 重定向到登录页面
    router.push('/login');
    
    console.log('[主应用] 退出登录状态已同步');
  } else {
    console.log(`[主应用] 不清除会话存储：当前标签页已有不同的用户/角色登录 (${sessionUserRole}/${sessionUserId})`);
  }
});

const app = createApp(App);
app.use(router); // 使用路由
app.mount('#app');
