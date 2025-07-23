import './assets/main.css';
import './assets/global.css';

import { createApp } from 'vue';
import App from './App.vue';
import router from './router'; // 导入路由
import { checkAuth, authState, navigateToDashboard } from './services/auth'; // 导入认证服务

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

const app = createApp(App);
app.use(router); // 使用路由
app.mount('#app');
