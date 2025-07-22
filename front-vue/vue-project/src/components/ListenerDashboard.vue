<template>
  <div class="dashboard-container">
    <h1>听众仪表盘</h1>
    <p>欢迎，听众！在这里参与您感兴趣的演讲。</p>

    <div class="dashboard-content">
      <aside class="sidebar">
        <nav>
          <ul>
            <li>
              <router-link to="/listener/dashboard/available">可参与演讲</router-link>
            </li>
            <li>
              <router-link to="/listener/dashboard/active">当前演讲</router-link>
            </li>
            <li>
              <router-link to="/listener/dashboard/current-questions">当前题目</router-link>
            </li>
            <li>
              <router-link to="/listener/dashboard/files">文件下载</router-link>
            </li>
            <li>
              <router-link to="/listener/dashboard/report">个人报告</router-link>
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
import { ref, provide } from 'vue';

// 选中的演讲ID，供子组件使用
const selectedPresentationId = ref(null);

// 提供给子组件使用
provide('selectedPresentationId', selectedPresentationId);
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

.presentation-list {
  display: grid;
  gap: 15px;
}

.presentation-item {
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

.join-button, .view-report-button {
  align-self: flex-end;
  margin-top: 10px;
}

.active-question {
  background-color: #f9f9f9;
  border: 1px solid #eee;
  border-radius: 8px;
  padding: 15px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.options {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.option-button {
  background-color: #6c757d; /* Different color for options */
  border-color: #6c757d;
  padding: 8px 15px;
  font-size: 10px;
}

.option-button:hover {
  background-color: #5a6268;
  border-color: #545b62;
}

.submit-answer-button {
  align-self: flex-end;
  margin-top: 15px;
}

.feedback-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.feedback-button {
  background-color: #ffc107; /* Different color for feedback */
  border-color: #ffc107;
  color: #333;
  padding: 8px 15px;
  font-size: 10px;
}

.feedback-button:hover {
  background-color: #e0a800;
  border-color: #d39e00;
}
</style>
