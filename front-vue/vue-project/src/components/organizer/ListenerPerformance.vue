<template>
  <div class="sub-dashboard-section">
    <h2>听众表现</h2>
    <div class="listener-performance-list">
      <div class="listener-item">
        <h3>听众: listener_one</h3>
        <p>已答题目: 2</p>
        <p>正确题目: 1</p>
        <p>正确率: 50%</p>
        <button class="view-report-button">查看详细报告</button>
      </div>
      <div class="listener-item">
        <h3>听众: listener_two</h3>
        <p>已答题目: 2</p>
        <p>正确题目: 2</p>
        <p>正确率: 100%</p>
        <button class="view-report-button">查看详细报告</button>
      </div>
      <!-- 更多听众表现项 -->
    </div>
  </div>
</template>

<script setup>
// 听众表现的逻辑
// 实际应用中会从后端获取数据并渲染
</script>

<style scoped>
.sub-dashboard-section {
  padding: 20px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

h2 {
  color: #4dc189;
  margin-bottom: 20px;
}

h3 {
  color: #333;
  margin-top: 0;
  margin-bottom: 10px;
}

.listener-performance-list {
  display: grid;
  gap: 15px;
}

.listener-item {
  background-color: #f9f9f9;
  border: 1px solid #eee;
  border-radius: 8px;
  padding: 15px;
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.listener-item p {
  font-size: 14px;
  margin-bottom: 5px;
}

.view-report-button {
  align-self: flex-end;
  border-radius: 20px;
  border: 1px solid #4dc189;
  background-color: #4dc189;
  color: #FFFFFF;
  font-size: 10px;
  font-weight: bold;
  padding: 8px 15px;
  letter-spacing: 1px;
  text-transform: uppercase;
  transition: transform 80ms ease-in;
  cursor: pointer;
  margin-top: 10px;
}

.view-report-button:active {
  transform: scale(0.95);
}
</style>
