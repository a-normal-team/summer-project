<template>
  <div class="personal-report">
    <h2>个人报告</h2>
    <div class="report-content">
      <div class="stats-section">
        <h3>总体统计</h3>
        <p>参与演讲数: 5</p>
        <p>总答题数: 25</p>
        <p>平均正确率: 75%</p>
      </div>
      <div class="improvement-section">
        <h3>建议改进</h3>
        <ul>
          <li>继续保持积极参与</li>
          <li>可以多关注框架设计相关的问题</li>
          <li>建议复习基础概念</li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup>
// 个人报告逻辑
</script>

<style scoped>
.personal-report {
  padding: 20px;
}

.report-content {
  margin-top: 20px;
}

.stats-section, .improvement-section {
  margin-bottom: 30px;
}

.improvement-section ul {
  list-style-type: disc;
  margin-left: 20px;
}
</style>
