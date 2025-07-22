<template>
  <div class="dashboard-container">
    <h1>演讲者仪表盘</h1>
    <p>欢迎，演讲者！在这里管理您的演讲和测验。</p>

    <div class="dashboard-content">
      <aside class="sidebar">
        <nav>
          <ul>
            <li>
              <router-link to="/speaker/dashboard/create">创建演讲</router-link>
            </li>
            <li>
              <router-link to="/speaker/dashboard/presentations">我的演讲</router-link>
            </li>
            <li>
              <router-link to="/speaker/dashboard/files">文件管理</router-link>
            </li>
            <li>
              <router-link to="/speaker/dashboard/quiz">题目管理</router-link>
            </li>
            <li>
              <router-link to="/speaker/dashboard/stats">演讲统计</router-link>
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
// 演讲者仪表盘的逻辑
// 实际应用中会从后端获取数据并渲染
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
  flex-grow: 1;
  overflow: hidden;
  height: calc(100% - 100px); /* 减去标题和欢迎文本的高度 */
  min-height: 0; /* 关键属性：确保flex子项可以正确计算滚动区域 */
  width: 100%; /* 确保占据全部可用宽度 */
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

h1 {
  text-align: center;
  color: #4dc189;
  margin-bottom: 30px;
}

h2 {
  color: #4dc189;
  border-bottom: 2px solid #eee;
  padding-bottom: 10px;
  margin-top: 40px;
  margin-bottom: 20px;
}

h3 {
  color: #333;
  margin-top: 20px;
  margin-bottom: 10px;
}

p {
  font-size: 16px;
  line-height: 1.5;
  margin-bottom: 10px;
}

.section {
  margin-bottom: 30px;
}

button {
  border-radius: 20px;
  border: 1px solid #4dc189;
  background-color: #4dc189;
  color: #FFFFFF;
  font-size: 12px;
  font-weight: bold;
  padding: 10px 20px;
  letter-spacing: 1px;
  text-transform: uppercase;
  transition: transform 80ms ease-in;
  cursor: pointer;
  margin-right: 10px;
  margin-bottom: 10px;
}

button:active {
  transform: scale(0.95);
}

.presentation-list, .file-list, .question-list {
  display: grid;
  gap: 15px;
}

.presentation-item, .file-item, .question-item, .active-question, .stats-item, .feedback-stats {
  background-color: #f9f9f9;
  border: 1px solid #eee;
  border-radius: 8px;
  padding: 15px;
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.presentation-item h3 {
  margin-top: 0;
  color: #333;
}

.manage-button, .upload-button, .generate-quiz-button, .deactivate-button {
  align-self: flex-start;
  margin-top: 10px;
}

.action-button {
  align-self: flex-end;
  font-size: 10px;
  padding: 8px 15px;
  margin-top: 5px;
}

.file-item, .question-item {
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
}

.file-item p, .question-item p {
  margin: 0;
}
</style>
