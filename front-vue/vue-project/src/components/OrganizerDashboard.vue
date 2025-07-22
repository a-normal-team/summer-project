<template>
  <div class="dashboard-container">
    <h1>组织者仪表盘</h1>
    <p>欢迎，组织者！在这里管理您的演讲活动。</p>

    <div class="dashboard-content">
      <aside class="sidebar">
        <nav>
          <ul>
            <li>
              <router-link to="/organizer/dashboard/presentations">全部演讲</router-link>
            </li>
            <li>
              <router-link to="/organizer/dashboard/overall-stats">整体统计</router-link>
            </li>
            <li>
              <router-link to="/organizer/dashboard/listener-performance">听众表现</router-link>
            </li>
          </ul>
        </nav>
      </aside>
      <main class="main-content">
        <router-view />
      </main>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router';
import { onMounted } from 'vue';

const router = useRouter();

onMounted(() => {
  // 默认跳转到我的演讲页面
  if (router.currentRoute.value.path === '/organizer/dashboard') {
    router.push('/organizer/dashboard/presentations');
  }
});
</script>

<style scoped>
.dashboard-container {
  font-family: 'Montserrat', sans-serif;
  padding: 20px;
  width: 800px; /* 固定宽度 */
  height: 80vh; /* 使用视窗高度单位而不是固定像素，提供更灵活的高度 */
  min-height: 500px; /* 最小高度确保在小屏幕上也有足够空间 */
  margin: 50px auto;
  background-color: #fff;
  border-radius: 10px;
  box-shadow: 0 14px 28px rgba(0, 0, 0, 0.25), 0 10px 10px rgba(0, 0, 0, 0.22);
  color: #333;
  display: flex;
  flex-direction: column;
}

h1 {
  text-align: center;
  color: #4dc189;
  margin-bottom: 30px;
}

p {
  text-align: center;
  font-size: 16px;
  line-height: 1.5;
  margin-bottom: 20px;
}

.dashboard-content {
  display: flex;
  gap: 20px;
  flex-grow: 1; /* 填充剩余空间 */
  overflow: hidden; /* 隐藏容器本身的溢出，但允许子元素滚动 */
  height: calc(100% - 100px); /* 减去标题和欢迎文本的高度 */
  width: 100%; /* 确保占据全部可用宽度 */
  min-height: 0; /* 关键属性：确保flex子项可以正确计算滚动区域 */
}

.sidebar {
  width: 200px;
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.sidebar nav ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.sidebar nav li {
  margin-bottom: 10px;
}

.sidebar nav a {
  display: block;
  padding: 10px 15px;
  background-color: #4dc189;
  color: #FFFFFF;
  text-decoration: none;
  border-radius: 5px;
  transition: background-color 0.3s ease;
  font-weight: bold;
}

.sidebar nav a:hover,
.sidebar nav a.router-link-active {
  background-color: #3aa875;
}

.main-content {
  flex-grow: 1;
  flex-basis: 0; /* 设置基准值为0，确保flex-grow能正确工作 */
  width: 0; /* 设置初始宽度为0，让flex-grow控制实际宽度 */
  padding: 20px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  overflow-y: auto; /* 允许垂直滚动 */
  height: 100%; /* 填满父容器高度 */
  display: flex; /* 确保子组件能正确填充空间 */
  min-height: 0; /* 关键属性：确保flex子项可以正确计算滚动区域 */
  position: relative; /* 为绝对定位子元素提供参考 */
}
</style>
