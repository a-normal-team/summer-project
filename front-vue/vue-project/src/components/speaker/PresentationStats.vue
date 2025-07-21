<template>
  <div class="sub-dashboard-section">
    <h2>演讲统计</h2>
    <div class="stats-grid">
      <div class="stats-item">
        <div class="stats-header">总览</div>
        <div class="stats-content">
          <div class="stat-row">
            <span class="stat-label">总作答人数:</span>
            <span class="stat-value">5</span>
          </div>
          <div class="stat-row">
            <span class="stat-label">正确人数:</span>
            <span class="stat-value">3</span>
          </div>
          <div class="stat-row">
            <span class="stat-label">正确率:</span>
            <span class="stat-value">60%</span>
          </div>
        </div>
      </div>
      <div class="stats-item">
        <div class="stats-header">选项分布</div>
        <div class="stats-content">
          <div class="option-distribution">
            <div class="option-item">
              <span class="option-label">微框架:</span>
              <span class="option-count">3</span>
            </div>
            <div class="option-item">
              <span class="option-label">全栈框架:</span>
              <span class="option-count">1</span>
            </div>
            <div class="option-item">
              <span class="option-label">前端框架:</span>
              <span class="option-count">1</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
// 统计逻辑
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

.stats-grid {
  display: grid;
  gap: 20px;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
}

.stats-item {
  background-color: #f9f9f9;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.stats-header {
  background-color: #4dc189;
  color: white;
  padding: 10px 15px;
  font-weight: bold;
}

.stats-content {
  padding: 15px;
}

.stat-row {
  display: flex;
  justify-content: space-between;
  padding: 8px 0;
  border-bottom: 1px solid #eee;
}

.stat-row:last-child {
  border-bottom: none;
}

.stat-label {
  color: #666;
}

.stat-value {
  font-weight: bold;
  color: #333;
}

.option-distribution {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.option-item {
  display: flex;
  justify-content: space-between;
  padding: 5px 0;
}

.option-label {
  color: #666;
}

.option-count {
  font-weight: bold;
  color: #333;
}
</style>
