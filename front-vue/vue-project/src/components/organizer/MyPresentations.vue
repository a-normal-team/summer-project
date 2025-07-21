<template>
  <div class="sub-dashboard-section">
    <h2>我的演讲</h2>
    <button class="create-button">创建新演讲</button>
    <div class="presentation-list">
      <div class="presentation-item">
        <h3>Spring Boot入门</h3>
        <p>这是一个关于 Flask 基础的介绍性演讲。</p>
        <p>演讲者: speaker_one</p>
        <p>状态: 进行中</p>
        <button class="manage-button">管理</button>
      </div>
      <!-- 更多演讲项 -->
    </div>
  </div>
</template>

<script setup>
// 我的演讲列表逻辑
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

.create-button {
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
  margin-bottom: 20px;
}

.create-button:active {
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

.manage-button {
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

.manage-button:active {
  transform: scale(0.95);
}
</style>
