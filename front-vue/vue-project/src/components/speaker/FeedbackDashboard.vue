<template>
  <div class="sub-dashboard-section">
    <div class="feedback-dashboard">
      <div class="header-section">
        <h2>反馈汇总</h2>
        <div class="time-filter">
          <button 
            v-for="period in timePeriods" 
            :key="period.value"
            class="filter-button"
            :class="{ active: selectedPeriod === period.value }"
            @click="selectedPeriod = period.value"
          >
            {{ period.label }}
          </button>
        </div>
      </div>

      <div class="dashboard-content">
        <div class="feedback-stats">
          <div class="stat-card total">
            <div class="stat-header">
              <span class="stat-icon">📊</span>
              <span class="stat-title">总反馈数</span>
            </div>
            <div class="stat-value">{{ totalFeedbacks }}</div>
          </div>

          <div 
            v-for="category in feedbackCategories" 
            :key="category.type"
            class="stat-card"
          >
            <div class="stat-header">
              <span class="stat-icon">{{ category.icon }}</span>
              <span class="stat-title">{{ category.label }}</span>
            </div>
            <div class="stat-value">{{ getFeedbackCount(category.type) }}</div>
            <div class="trend" :class="getFeedbackTrend(category.type).type">
              {{ getFeedbackTrend(category.type).value }}%
            </div>
          </div>
        </div>

        <div class="feedback-chart">
          <h3>反馈趋势</h3>
          <div class="chart-container">
            <!-- 这里可以集成图表库，如 ECharts -->
            <div class="placeholder-chart">
              图表区域
            </div>
          </div>
        </div>

        <div class="feedback-details">
          <h3>详细反馈</h3>
          <div class="feedback-list">
            <div 
              v-for="feedback in sortedFeedbacks" 
              :key="feedback.id"
              class="feedback-item"
              :class="feedback.type"
            >
              <div class="feedback-header">
                <span class="feedback-type">{{ getFeedbackLabel(feedback.type) }}</span>
                <span class="feedback-time">{{ formatTime(feedback.time) }}</span>
              </div>
              <div class="feedback-content">
                {{ feedback.content }}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';

const timePeriods = [
  { label: '实时', value: 'realtime' },
  { label: '今天', value: 'today' },
  { label: '本周', value: 'week' },
  { label: '全部', value: 'all' }
];

const feedbackCategories = [
  { type: 'too-fast', label: '讲得太快', icon: '⚡' },
  { type: 'too-slow', label: '讲得太慢', icon: '🐌' },
  { type: 'boring', label: '内容乏味', icon: '😴' },
  { type: 'poor-quality', label: '题目质量差', icon: '👎' },
  { type: 'confusing', label: '内容难懂', icon: '🤔' },
  { type: 'interesting', label: '内容有趣', icon: '👍' }
];

const selectedPeriod = ref('realtime');
const feedbacks = ref([]); // 假设这里会通过 props 或 API 获取数据

const totalFeedbacks = computed(() => feedbacks.value.length);

const sortedFeedbacks = computed(() => {
  return [...feedbacks.value].sort((a, b) => b.time - a.time);
});

const getFeedbackCount = (type) => {
  return feedbacks.value.filter(f => f.type === type).length;
};

const getFeedbackTrend = (type) => {
  // 这里应该实现实际的趋势计算逻辑
  const trend = Math.random() * 20 - 10; // 示例：随机生成-10到10的趋势
  return {
    value: Math.abs(trend).toFixed(1),
    type: trend > 0 ? 'up' : 'down'
  };
};

const getFeedbackLabel = (type) => {
  const category = feedbackCategories.find(c => c.type === type);
  return category ? category.label : type;
};

const formatTime = (time) => {
  return new Date(time).toLocaleString('zh-CN', {
    hour: '2-digit',
    minute: '2-digit'
  });
};
</script>

<style scoped>
.feedback-dashboard {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.header-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

h2 {
  color: #4dc189;
  margin: 0;
}

.time-filter {
  display: flex;
  gap: 10px;
}

.filter-button {
  padding: 6px 12px;
  border-radius: 15px;
  border: 1px solid #ddd;
  background-color: #fff;
  color: #666;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.filter-button:hover {
  border-color: #4dc189;
  color: #4dc189;
}

.filter-button.active {
  background-color: #4dc189;
  border-color: #4dc189;
  color: #fff;
}

.dashboard-content {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.feedback-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 15px;
}

.stat-card {
  background-color: #f9f9f9;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.stat-card.total {
  background-color: #4dc189;
  color: white;
}

.stat-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 10px;
}

.stat-icon {
  font-size: 24px;
}

.stat-title {
  font-size: 14px;
  color: #666;
}

.stat-card.total .stat-title {
  color: white;
}

.stat-value {
  font-size: 24px;
  font-weight: bold;
  color: #333;
  margin: 10px 0;
}

.stat-card.total .stat-value {
  color: white;
}

.trend {
  font-size: 12px;
  padding: 2px 6px;
  border-radius: 10px;
  display: inline-block;
}

.trend.up {
  background-color: #d4edda;
  color: #28a745;
}

.trend.down {
  background-color: #f8d7da;
  color: #dc3545;
}

.feedback-chart {
  background-color: #f9f9f9;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

h3 {
  color: #333;
  margin-bottom: 15px;
}

.chart-container {
  height: 300px;
  background-color: #fff;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #666;
}

.feedback-details {
  background-color: #f9f9f9;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.feedback-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.feedback-item {
  background-color: #fff;
  border-radius: 6px;
  padding: 15px;
  border-left: 4px solid #ddd;
}

.feedback-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
}

.feedback-type {
  font-weight: bold;
  color: #333;
}

.feedback-time {
  color: #666;
  font-size: 12px;
}

.feedback-content {
  color: #666;
  font-size: 14px;
}

/* 反馈类型样式 */
.feedback-item.too-fast {
  border-left-color: #ffc107;
}

.feedback-item.too-slow {
  border-left-color: #17a2b8;
}

.feedback-item.boring,
.feedback-item.poor-quality {
  border-left-color: #dc3545;
}

.feedback-item.confusing {
  border-left-color: #6c757d;
}

.feedback-item.interesting {
  border-left-color: #28a745;
}
</style>
