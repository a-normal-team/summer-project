<template>
  <div class="sub-dashboard-section">
    <h2>文件管理</h2>
    <button class="action-button upload-button">上传文件</button>
    <div class="file-list">
      <div class="file-item">
        <div class="file-info">
          <p class="file-name">SpringBoot.pptx</p>
          <p class="file-meta">上传时间：2025-07-21</p>
        </div>
        <div class="file-actions">
          <button class="action-button">查看</button>
          <button class="action-button danger">删除</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
// 文件管理逻辑
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

.upload-button {
  margin-bottom: 20px;
  width: auto;
}

.file-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.file-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #f9f9f9;
  padding: 15px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.file-info {
  flex-grow: 1;
}

.file-name {
  font-weight: bold;
  color: #333;
  margin-bottom: 5px;
}

.file-meta {
  font-size: 12px;
  color: #666;
}

.file-actions {
  display: flex;
  gap: 10px;
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

