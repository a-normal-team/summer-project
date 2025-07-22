<template>
  <div class="sub-dashboard-section">
    <h2>听众表现</h2>
    
    <div v-if="!selectedPresentationId" class="no-selection">
      <p>请先在"所有演讲"中选择一个演讲进行查看</p>
    </div>
    
    <div v-else-if="loading" class="loading-state">
      <p>加载中...</p>
    </div>
    
    <div v-else-if="error" class="error-state">
      <p>{{ error }}</p>
      <button @click="fetchListenerPerformance" class="retry-button">重试</button>
    </div>
    
    <div v-else>
      <div class="presentation-header" v-if="presentationDetails">
        <h3>{{ presentationDetails.title }}</h3>
        <p>演讲者: {{ presentationDetails.speaker || '未分配' }}</p>
      </div>
      
      <div v-if="listeners.length === 0" class="empty-state">
        <p>该演讲暂无听众参与</p>
      </div>
      
      <div v-else class="listener-performance-list">
        <div v-for="(listener, index) in listeners" :key="index" class="listener-item">
          <h3>听众: {{ listener.username }}</h3>
          <p>已答题目: {{ listener.answeredQuizzes || 0 }}</p>
          <p>正确题目: {{ listener.correctAnswers || 0 }}</p>
          <p>正确率: {{ listener.accuracy ? `${listener.accuracy}%` : 'N/A' }}</p>
          <p>最后活动时间: {{ formatDateTime(listener.lastActivity) }}</p>
          <div class="quiz-answers" v-if="listener.quizAnswers && listener.quizAnswers.length > 0">
            <h4>题目回答详情:</h4>
            <div v-for="(answer, i) in listener.quizAnswers" :key="i" class="quiz-answer-item">
              <p>题目 #{{ i + 1 }}: {{ answer.isCorrect ? '✓ 正确' : '✗ 错误' }}</p>
              <p class="answer-time">回答时间: {{ formatDateTime(answer.answeredAt) }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import { getPresentationById, getListenerPerformance } from '../../services/presentation';

// 状态变量
const selectedPresentationId = ref(null);
const presentationDetails = ref(null);
const listeners = ref([]);
const loading = ref(false);
const error = ref(null);

// 页面加载时获取已选择的演讲ID
onMounted(() => {
  const storedId = localStorage.getItem('selectedPresentationId');
  if (storedId) {
    selectedPresentationId.value = parseInt(storedId);
    fetchPresentationDetails();
    fetchListenerPerformance();
  }
});

// 监听选中的演讲ID变化
watch(selectedPresentationId, (newValue) => {
  if (newValue) {
    fetchPresentationDetails();
    fetchListenerPerformance();
  } else {
    presentationDetails.value = null;
    listeners.value = [];
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

// 获取听众表现数据
const fetchListenerPerformance = async () => {
  if (!selectedPresentationId.value) return;
  
  try {
    loading.value = true;
    error.value = null;
    
    const data = await getListenerPerformance(selectedPresentationId.value);
    listeners.value = Array.isArray(data) ? data : [];
  } catch (err) {
    console.error('获取听众表现数据失败:', err);
    error.value = '获取听众表现数据失败: ' + (err.message || '未知错误');
  } finally {
    loading.value = false;
  }
};

// 格式化日期时间
const formatDateTime = (dateTimeStr) => {
  if (!dateTimeStr) return '未知';
  
  try {
    const date = new Date(dateTimeStr);
    return new Intl.DateTimeFormat('zh-CN', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit',
      hour12: false
    }).format(date);
  } catch (err) {
    return dateTimeStr;
  }
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
  margin-top: 0;
  margin-bottom: 10px;
}

.listener-performance-list {
  display: grid;
  gap: 15px;
}

.listener-item {
  background-color: #f9f9f9;
  border: 1px solid #eee;
  border-radius: 8px;
  padding: 15px;
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.listener-item p {
  font-size: 14px;
  margin-bottom: 5px;
}

.view-report-button {
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

.view-report-button:active {
  transform: scale(0.95);
}
</style>
