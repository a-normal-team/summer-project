<template>
  <div class="sub-dashboard-section">
    <h2>整体统计</h2>
    
    <div v-if="!selectedPresentationId" class="no-selection">
      <p>请先在"所有演讲"中选择一个演讲进行查看</p>
    </div>
    
    <div v-else-if="loading" class="loading-state">
      <p>加载中...</p>
    </div>
    
    <div v-else-if="error" class="error-state">
      <p>{{ error }}</p>
      <button @click="fetchStats" class="retry-button">重试</button>
    </div>
    
    <div v-else class="stats-container">
      <div class="presentation-header">
        <h3>{{ presentationDetails?.title }}</h3>
        <p>演讲者: {{ presentationDetails?.speaker || '未分配' }}</p>
        <p>状态: {{ getStatusText(presentationDetails?.status) }}</p>
      </div>
      
      <div class="stats-grid">
        <div class="stat-card">
          <h3>总参与人数</h3>
          <p class="stat-value">{{ stats.totalListeners || 0 }}</p>
        </div>
        <div class="stat-card">
          <h3>平均正确率</h3>
          <p class="stat-value">{{ stats.averageAccuracy ? `${stats.averageAccuracy}%` : 'N/A' }}</p>
        </div>
        <div class="stat-card">
          <h3>总题目数</h3>
          <p class="stat-value">{{ stats.totalQuizzes || 0 }}</p>
        </div>
        <div class="stat-card">
          <h3>已答题目</h3>
          <p class="stat-value">{{ stats.answeredQuizzes || 0 }}</p>
        </div>
      </div>

      <div v-if="stats.quizStats && stats.quizStats.length > 0">
        <h3>题目统计</h3>
        <div class="quiz-stats-list">
          <div v-for="(quiz, index) in stats.quizStats" :key="index" class="quiz-stat-item">
            <h4>题目 #{{ index + 1 }}</h4>
            <p>{{ quiz.question }}</p>
            <p>正确率: {{ quiz.accuracy }}%</p>
            <p>答题人数: {{ quiz.totalAnswers }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import { getPresentationById, getPresentationStats } from '../../services/presentation';

// 状态变量
const selectedPresentationId = ref(null);
const presentationDetails = ref(null);
const stats = ref({
  totalListeners: 0,
  averageAccuracy: 0,
  totalQuizzes: 0,
  answeredQuizzes: 0,
  quizStats: []
});
const loading = ref(false);
const error = ref(null);

// 页面加载时获取已选择的演讲ID
onMounted(() => {
  const storedId = localStorage.getItem('selectedPresentationId');
  if (storedId) {
    selectedPresentationId.value = parseInt(storedId);
    fetchPresentationDetails();
    fetchStats();
  }
});

// 监听选中的演讲ID变化
watch(selectedPresentationId, (newValue) => {
  if (newValue) {
    fetchPresentationDetails();
    fetchStats();
  } else {
    presentationDetails.value = null;
    stats.value = {
      totalListeners: 0,
      averageAccuracy: 0,
      totalQuizzes: 0,
      answeredQuizzes: 0,
      quizStats: []
    };
  }
});

// 获取演讲详情
const fetchPresentationDetails = async () => {
  if (!selectedPresentationId.value) return;
  
  try {
    loading.value = true;
    error.value = null;
    
    // 以organizer角色获取演讲详情
    const data = await getPresentationById(selectedPresentationId.value, 'organizer');
    presentationDetails.value = data;
  } catch (err) {
    console.error('获取演讲详情失败:', err);
    error.value = '获取演讲详情失败: ' + (err.message || '未知错误');
  } finally {
    loading.value = false;
  }
};

// 获取统计数据
const fetchStats = async () => {
  if (!selectedPresentationId.value) return;
  
  try {
    loading.value = true;
    error.value = null;
    
    const data = await getPresentationStats(selectedPresentationId.value);
    stats.value = data;
  } catch (err) {
    console.error('获取统计数据失败:', err);
    error.value = '获取统计数据失败: ' + (err.message || '未知错误');
  } finally {
    loading.value = false;
  }
};

// 获取状态文本
const getStatusText = (status) => {
  const statusMap = {
    'pending': '计划中',
    'active': '进行中',
    'completed': '已完成'
  };
  return statusMap[status] || status || '未知';
};
</script>

<style scoped>
.sub-dashboard-section {
  padding: 20px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  height: 100%; /* 填满父容器高度 */
  width: 100%; /* 填满父容器宽度 */
  overflow-y: auto; /* 允许内容垂直滚动 */
  display: flex;
  flex-direction: column;
  flex: 1; /* 让组件填满父容器的剩余空间 */
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
