<template>
  <div class="sub-dashboard-section">
    <h2>整体统计</h2>
    <div class="stats-grid">
      <div class="stat-card">
        <h3>总参与人数</h3>
        <p class="stat-value">3</p>
      </div>
      <div class="stat-card">
        <h3>平均正确率</h3>
        <p class="stat-value">75%</p>
      </div>
    </div>

    <h3>我的演讲概览</h3>
    <div class="presentation-list">
      <div class="presentation-item">
        <h4>Spring Boot入门</h4>
        <p>演讲者: speaker_one</p>
        <p>状态: 进行中</p>
        <p>参与人数: 3</p>
        <p>平均正确率: 75%</p>
      </div>
      <!-- 更多演讲概览 -->
    </div>
  </div>
</template>

<script setup>
// 整体统计的逻辑
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
  margin-top: 30px;
  margin-bottom: 15px;
  border-bottom: 1px solid #eee;
  padding-bottom: 5px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.stat-card {
  background-color: #f0f8f4; /* Light green background */
  border: 1px solid #d4edda;
  border-radius: 8px;
  padding: 20px;
  text-align: center;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
}

.stat-card h3 {
  margin-top: 0;
  color: #4dc189;
  font-size: 18px;
  border-bottom: none;
  padding-bottom: 0;
}

.stat-value {
  font-size: 36px;
  font-weight: bold;
  color: #333;
  margin-top: 10px;
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

.presentation-item h4 {
  margin-top: 0;
  color: #333;
}

.presentation-item p {
  font-size: 14px;
  margin-bottom: 5px;
}
</style>
