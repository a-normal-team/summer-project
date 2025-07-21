<template>
  <div class="sub-dashboard-section">
    <h2>可参与的演讲</h2>
    <div class="presentation-list">
      <div class="presentation-item">
        <h3>Spring Boot入门</h3>
        <p>这是一个关于 Flask 基础的介绍性演讲。</p>
        <p>演讲者: speaker_one</p>
        <button class="join-button">参与演讲</button>
      </div>
    </div>
  </div>
</template>

<script setup>
// 可用演讲列表逻辑
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

.presentation-list {
  display: grid;
  gap: 20px;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
}

.presentation-item {
  background-color: #f9f9f9;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.presentation-item h3 {
  color: #333;
  margin-bottom: 10px;
}

.presentation-item p {
  color: #666;
  margin-bottom: 8px;
  font-size: 14px;
}

.join-button {
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
  width: 100%;
  margin-top: 10px;
}

.join-button:hover {
  background-color: #3aa875;
  transform: translateY(-1px);
}
</style>
