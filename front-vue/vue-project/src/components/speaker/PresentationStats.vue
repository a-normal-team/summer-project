<template>
  <div class="sub-dashboard-section">
    <h2>演讲统计</h2>
    
    <!-- 加载状态 -->
    <div v-if="loading" class="loading-state">
      <div class="spinner"></div>
      <p>正在加载数据...</p>
    </div>
    
    <!-- 错误状态 -->
    <div v-else-if="error" class="error-state">
      <p class="error-message">{{ error }}</p>
      <button @click="checkSelectedPresentation" class="retry-button">重试</button>
    </div>
    
    <!-- 未选择演讲 -->
    <div v-else-if="!selectedPresentation" class="no-selection">
      <p>请先选择一个演讲</p>
      <router-link to="/speaker/dashboard/presentations" class="nav-link">选择演讲</router-link>
    </div>
    
    <!-- 有演讲数据 -->
    <div v-else>
      <div class="presentation-info">
        <h3>当前选中: {{ selectedPresentation.title }}</h3>
        <p>{{ selectedPresentation.description }}</p>
      </div>
      
      <div class="stats-section">
        <h3>演讲数据总览</h3>
        <div class="stats-grid">
          <div class="stats-item">
            <div class="stats-header">听众参与情况</div>
            <div class="stats-content">
              <div class="stat-row">
                <span class="stat-label">总听众人数:</span>
                <span class="stat-value">{{ stats.totalListeners }}</span>
              </div>
              <div class="stat-row">
                <span class="stat-label">活跃参与人数:</span>
                <span class="stat-value">{{ stats.activeListeners }}</span>
              </div>
              <div class="stat-row">
                <span class="stat-label">参与率:</span>
                <span class="stat-value">{{ stats.participationRate }}%</span>
              </div>
            </div>
          </div>
          
          <div class="stats-item">
            <div class="stats-header">测验情况</div>
            <div class="stats-content">
              <div class="stat-row">
                <span class="stat-label">测验总数:</span>
                <span class="stat-value">{{ stats.totalQuizzes }}</span>
              </div>
              <div class="stat-row">
                <span class="stat-label">平均正确率:</span>
                <span class="stat-value">{{ stats.averageCorrectRate }}%</span>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <div class="quiz-stats" v-if="quizResults.length > 0">
        <h3>测验结果详情</h3>
        <div class="quiz-item" v-for="(quiz, index) in quizResults" :key="index">
          <h4>测验 {{ index + 1 }}: {{ quiz.question }}</h4>
          <div class="stat-row">
            <span class="stat-label">总作答人数:</span>
            <span class="stat-value">{{ quiz.totalResponses }}</span>
          </div>
          <div class="stat-row">
            <span class="stat-label">正确人数:</span>
            <span class="stat-value">{{ quiz.correctResponses }}</span>
          </div>
          <div class="stat-row">
            <span class="stat-label">正确率:</span>
            <span class="stat-value">{{ quiz.correctRate }}%</span>
          </div>
          
          <div class="option-distribution">
            <h5>选项分布:</h5>
            <div class="option-item" v-for="(count, option) in quiz.optionDistribution" :key="option">
              <span class="option-label">{{ option }}:</span>
              <span class="option-count">{{ count }}</span>
              <div class="option-bar" :style="{ width: (count / quiz.totalResponses * 100) + '%' }"></div>
            </div>
          </div>
        </div>
      </div>
      <div v-else class="empty-stats">
        <p>暂无测验数据</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRouter } from 'vue-router';
import { getPresentationById } from '../../services/presentation';
import { getPresentationStats } from '../../services/quiz';
import { authState } from '../../services/auth';

const router = useRouter();
const selectedPresentation = ref(null);
const loading = ref(false);
const error = ref(null);
const presentationStats = ref(null);

// 计算出格式化的统计数据
const stats = computed(() => {
  if (!presentationStats.value) {
    return {
      totalListeners: 0,
      activeListeners: 0,
      participationRate: 0,
      totalQuizzes: 0,
      averageCorrectRate: 0
    };
  }
  
  const data = presentationStats.value;
  return {
    totalListeners: data.total_listeners || 0,
    activeListeners: data.active_listeners || 0,
    participationRate: data.total_listeners ? ((data.active_listeners / data.total_listeners) * 100).toFixed(1) : 0,
    totalQuizzes: data.total_questions || 0,
    averageCorrectRate: data.average_correct_rate ? data.average_correct_rate.toFixed(1) : 0
  };
});

// 问题统计数据
const quizResults = computed(() => {
  if (!presentationStats.value || !presentationStats.value.questions) {
    return [];
  }
  
  return presentationStats.value.questions.map(q => {
    // 计算选项分布
    const optionDistribution = {};
    if (q.option_distribution) {
      for (const option in q.option_distribution) {
        optionDistribution[option] = q.option_distribution[option];
      }
    }
    
    return {
      question: q.content,
      totalResponses: q.total_responses || 0,
      correctResponses: q.correct_responses || 0,
      correctRate: q.total_responses ? ((q.correct_responses / q.total_responses) * 100).toFixed(1) : 0,
      optionDistribution: optionDistribution
    };
  });
});

// 页面加载时检查是否有选中的演讲
onMounted(() => {
  checkSelectedPresentation();
});

// 检查是否有选中的演讲
const checkSelectedPresentation = async () => {
  const storedSelectedId = localStorage.getItem('selectedPresentationId');
  if (!storedSelectedId) return;

  loading.value = true;
  error.value = null;
  
  try {
    // 从API获取演讲详情
    const presentation = await getPresentationById(storedSelectedId);
    selectedPresentation.value = presentation;
    
    // 获取该演讲的统计数据
    await loadPresentationStats(selectedPresentation.value.id);
  } catch (err) {
    console.error('获取演讲详情失败:', err);
    error.value = err.message || '获取演讲详情失败，请稍后再试';
  } finally {
    loading.value = false;
  }
};

// 加载演讲的统计数据
const loadPresentationStats = async (presentationId) => {
  loading.value = true;
  error.value = null;
  
  try {
    // 从API获取演讲统计
    const stats = await getPresentationStats(presentationId);
    presentationStats.value = stats;
    console.log('获取演讲统计:', stats);
  } catch (err) {
    console.error('获取演讲统计失败:', err);
    error.value = err.message || '获取演讲统计失败，请稍后再试';
    presentationStats.value = null;
  } finally {
    loading.value = false;
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

.no-selection, .empty-stats {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 30px 0;
}

.nav-link {
  margin-top: 15px;
  text-decoration: none;
  background-color: #4dc189;
  color: white;
  padding: 10px 20px;
  border-radius: 20px;
  font-weight: bold;
  transition: all 0.3s ease;
}

.nav-link:hover {
  background-color: #3aa875;
  transform: translateY(-1px);
}

.presentation-info {
  background-color: #f9f9f9;
  padding: 15px;
  border-radius: 8px;
  margin-bottom: 20px;
  border-left: 4px solid #4dc189;
}

.presentation-info h3 {
  margin-top: 0;
  color: #333;
  margin-bottom: 5px;
}

.presentation-info p {
  margin: 0;
  color: #666;
}

.stats-section {
  margin-bottom: 30px;
}

.quiz-stats {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.quiz-item {
  background-color: #f9f9f9;
  border-radius: 8px;
  padding: 15px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.quiz-item h4 {
  margin-top: 0;
  color: #333;
  margin-bottom: 10px;
  border-bottom: 1px solid #eee;
  padding-bottom: 5px;
}

.quiz-item h5 {
  margin: 15px 0 10px;
  color: #555;
}

.option-distribution {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-top: 10px;
}

.option-item {
  display: flex;
  align-items: center;
  padding: 5px 0;
  position: relative;
}

.option-label {
  color: #666;
  width: 120px;
}

.option-count {
  font-weight: bold;
  color: #333;
  width: 30px;
  margin-right: 10px;
}

.option-bar {
  height: 12px;
  background-color: #4dc189;
  border-radius: 6px;
  position: relative;
  min-width: 5px;
  max-width: calc(100% - 170px);
  transition: width 0.5s ease;
}

/* 加载状态 */
.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px 0;
}

.spinner {
  width: 40px;
  height: 40px;
  margin-bottom: 15px;
  border: 4px solid rgba(77, 193, 137, 0.2);
  border-top-color: #4dc189;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* 错误状态 */
.error-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 30px;
  background-color: rgba(255, 226, 226, 0.3);
  border-radius: 8px;
  border: 1px solid #ff9999;
  margin: 20px 0;
}

.error-message {
  color: #cc3333;
  text-align: center;
  margin-bottom: 15px;
}

.retry-button {
  background-color: #4dc189;
  color: white;
  border: none;
  border-radius: 20px;
  padding: 8px 20px;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.2s ease;
}

.retry-button:hover {
  background-color: #3aa875;
  transform: translateY(-1px);
}
</style>
