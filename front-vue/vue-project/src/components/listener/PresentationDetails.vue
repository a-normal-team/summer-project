<template>
  <div class="sub-dashboard-section">
    <div class="presentation-details">
      <div class="header-section">
        <h2>{{ presentation.title }}</h2>
        <div class="presentation-meta">
          <div class="meta-item">
            <span class="label">演讲者</span>
            <span class="value">{{ presentation.speaker }}</span>
          </div>
          <div class="meta-item">
            <span class="label">时间</span>
            <span class="value">{{ formatDateTime(presentation.startTime) }}</span>
          </div>
          <div class="meta-item">
            <span class="label">状态</span>
            <span class="status-badge" :class="presentation.status">
              {{ getStatusText(presentation.status) }}
            </span>
          </div>
        </div>
      </div>

      <div class="content-section">
        <div class="description-card">
          <h3>演讲简介</h3>
          <p>{{ presentation.description }}</p>
        </div>

        <div class="materials-card" v-if="presentation.materials?.length">
          <h3>相关资料</h3>
          <div class="materials-list">
            <div v-for="material in presentation.materials" :key="material.id" class="material-item">
              <span class="material-icon">📄</span>
              <span class="material-name">{{ material.name }}</span>
              <button class="action-button small" @click="downloadMaterial(material)">
                下载
              </button>
            </div>
          </div>
        </div>

        <div class="stats-card" v-if="presentation.status !== 'upcoming'">
          <h3>个人统计</h3>
          <div class="stats-grid">
            <div class="stat-item">
              <span class="stat-value">{{ stats.totalQuestions }}</span>
              <span class="stat-label">总题数</span>
            </div>
            <div class="stat-item">
              <span class="stat-value">{{ stats.correctAnswers }}</span>
              <span class="stat-label">答对题数</span>
            </div>
            <div class="stat-item">
              <span class="stat-value">{{ stats.correctRate }}%</span>
              <span class="stat-label">正确率</span>
            </div>
            <div class="stat-item">
              <span class="stat-value">{{ stats.ranking }}</span>
              <span class="stat-label">排名</span>
            </div>
          </div>
        </div>
      </div>

      <div class="action-section">
        <button 
          v-if="presentation.status === 'upcoming'" 
          class="action-button primary"
          @click="joinPresentation"
        >
          加入演讲
        </button>
        <button 
          v-if="presentation.status === 'completed'" 
          class="action-button"
          @click="viewReport"
        >
          查看完整报告
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineProps } from 'vue';

const props = defineProps({
  presentation: {
    type: Object,
    required: true
  },
  stats: {
    type: Object,
    default: () => ({
      totalQuestions: 0,
      correctAnswers: 0,
      correctRate: 0,
      ranking: 0
    })
  }
});

const formatDateTime = (dateTime) => {
  return new Date(dateTime).toLocaleString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  });
};

const getStatusText = (status) => {
  const statusMap = {
    'upcoming': '即将开始',
    'ongoing': '进行中',
    'completed': '已结束'
  };
  return statusMap[status] || status;
};

const downloadMaterial = (material) => {
  // TODO: 实现文件下载逻辑
  console.log('下载文件:', material);
};

const joinPresentation = () => {
  // TODO: 实现加入演讲逻辑
  console.log('加入演讲');
};

const viewReport = () => {
  // TODO: 实现查看报告逻辑
  console.log('查看报告');
};
</script>

<style scoped>
.presentation-details {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.header-section h2 {
  color: #4dc189;
  margin-bottom: 20px;
}

.presentation-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  margin-bottom: 20px;
}

.meta-item {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.label {
  color: #666;
  font-size: 14px;
}

.value {
  color: #333;
  font-weight: bold;
}

.status-badge {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: bold;
  color: white;
}

.status-badge.upcoming {
  background-color: #17a2b8;
}

.status-badge.ongoing {
  background-color: #28a745;
}

.status-badge.completed {
  background-color: #6c757d;
}

.content-section {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.description-card,
.materials-card,
.stats-card {
  background-color: #f9f9f9;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.description-card h3,
.materials-card h3,
.stats-card h3 {
  color: #333;
  margin-bottom: 15px;
}

.description-card p {
  color: #666;
  line-height: 1.6;
}

.materials-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.material-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px;
  background-color: #fff;
  border-radius: 6px;
  border: 1px solid #eee;
}

.material-icon {
  font-size: 20px;
}

.material-name {
  flex-grow: 1;
  color: #333;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: 15px;
}

.stat-item {
  text-align: center;
  padding: 15px;
  background-color: #fff;
  border-radius: 6px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.stat-value {
  display: block;
  font-size: 24px;
  font-weight: bold;
  color: #4dc189;
  margin-bottom: 5px;
}

.stat-label {
  display: block;
  font-size: 14px;
  color: #666;
}

.action-section {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 20px;
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

.action-button.small {
  padding: 4px 8px;
  font-size: 12px;
}

.action-button.primary {
  background-color: #28a745;
  border-color: #28a745;
}

.action-button.primary:hover {
  background-color: #218838;
  border-color: #1e7e34;
}
</style>
