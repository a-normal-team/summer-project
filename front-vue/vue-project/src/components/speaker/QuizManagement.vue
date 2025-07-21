<template>
  <div class="sub-dashboard-section">
    <h2>题目管理</h2>
    <button class="action-button generate-button">生成随堂测验</button>
    <div class="quiz-list">
      <div class="quiz-item">
        <h3>当前活跃题目:</h3>
        <div class="question-content">
          <p class="question-text">Flask 是一个什么类型的框架？</p>
          <p class="options-text">选项: 微框架, 全栈框架, 前端框架, 数据库框架</p>
        </div>
        <button class="action-button danger">停用题目</button>
      </div>
    </div>
  </div>
</template>

<script setup>
// 题目管理逻辑
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

.generate-button {
  margin-bottom: 20px;
  width: auto;
}

.quiz-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.quiz-item {
  background-color: #f9f9f9;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.quiz-item h3 {
  color: #333;
  margin-bottom: 15px;
}

.question-content {
  margin-bottom: 15px;
}

.question-text {
  font-weight: bold;
  color: #333;
  margin-bottom: 10px;
}

.options-text {
  color: #666;
  font-size: 14px;
}

.action-button {
  border-radius: 20px;
  border: 1px solid #4dc189;
  background-color: #4dc189;
  color: #FFFFFF;
  font-size: 12px;
  font-weight: bold;
  padding: 8px 16px;
  letter-spacing: 1px;
  text-transform: uppercase;
  transition: all 0.3s ease;
  cursor: pointer;
}

.action-button:hover {
  background-color: #3aa875;
  transform: translateY(-1px);
}

.action-button.danger {
  background-color: #dc3545;
  border-color: #dc3545;
}

.action-button.danger:hover {
  background-color: #bb2d3b;
}
</style>
