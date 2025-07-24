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
                <span class="stat-label">总答题数:</span>
                <span class="stat-value">{{ stats.totalAnswers }}</span>
              </div>
              <div class="stat-row">
                <span class="stat-label">平均每题作答:</span>
                <span class="stat-value">{{ stats.answersPerQuestion }}</span>
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
        <h3>测验结果详情 (共{{ quizResults.length }}题)</h3>
        <div class="quiz-item" v-for="(quiz, index) in quizResults" :key="index">
          <div class="quiz-header">
            <h4>测验 {{ index + 1 }}: {{ quiz.question }}</h4>
            <div class="quiz-status" :class="{ 'high-response': quiz.totalResponses > 0 }">
              {{ quiz.totalResponses > 0 ? '已有答题' : '暂无答题' }}
            </div>
          </div>
          
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
            <span class="stat-value" :class="{ 
              'high-rate': parseFloat(quiz.correctRate) > 80, 
              'medium-rate': parseFloat(quiz.correctRate) > 50 && parseFloat(quiz.correctRate) <= 80,
              'low-rate': parseFloat(quiz.correctRate) <= 50
            }">{{ quiz.correctRate }}%</span>
          </div>
          
          <div class="option-distribution" v-if="quiz.totalResponses > 0">
            <h5>选项分布:</h5>
            <div class="option-item" v-for="(count, option) in quiz.optionDistribution" :key="option">
              <span class="option-label">{{ option }}:</span>
              <span class="option-count">{{ count }}</span>
              <div class="option-bar" :style="{ width: (count / quiz.totalResponses * 100) + '%' }"></div>
            </div>
          </div>
          <div class="option-distribution" v-else>
            <p class="no-data-message">暂无选项分布数据</p>
          </div>
        </div>
      </div>
      
      <!-- 听众表现详情 -->
      <div class="listener-performance" v-if="listenerPerformance.length > 0">
        <h3>听众表现详情</h3>
        <table class="performance-table">
          <thead>
            <tr>
              <th>用户名</th>
              <th>回答问题数</th>
              <th>正确答案数</th>
              <th>正确率</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="listener in listenerPerformance" :key="listener.listener_id">
              <td>{{ listener.listener_username }}</td>
              <td>{{ listener.answered_questions }}</td>
              <td>{{ listener.correct_answers }}</td>
              <td>{{ listener.accuracy_rate }}</td>
            </tr>
          </tbody>
        </table>
      </div>
      <div v-else-if="!loading" class="empty-stats">
        <p>暂无听众表现数据</p>
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
  
  // 计算基于listener_performance的活跃听众数量
  let activeListenersCount = data.active_listeners || 0;
  
  // 计算总听众人数 - 优先使用total_participants，如果不存在则使用total_listeners
  let totalListenersCount = data.total_participants || data.total_listeners || 0;
  
  // 如果存在listener_performance数据，则使用它的长度作为活跃听众数
  if (data.listener_performance && Array.isArray(data.listener_performance) && data.listener_performance.length > 0) {
    activeListenersCount = data.listener_performance.length;
    console.log('使用listener_performance数据更新活跃听众数:', activeListenersCount);
    
    // 如果没有有效的总听众数据，但有活跃听众数据，则将总听众数至少设置为活跃听众数
    if (totalListenersCount === 0 || totalListenersCount < activeListenersCount) {
      totalListenersCount = activeListenersCount;
      console.log('更新总听众人数为活跃听众数:', totalListenersCount);
    }
  }
  
  // 获取更多测验情况相关数据
  const totalQuestionsInPresentation = data.total_questions_in_presentation || data.total_questions || 0;
  const totalAnswersSubmitted = data.total_answers_submitted || 0;
  const averageCorrectRate = data.average_correct_rate_across_all_questions || 
                            data.average_correct_rate || 
                            '0';
  
  return {
    // 听众数据
    totalListeners: totalListenersCount,
    activeListeners: activeListenersCount,
    participationRate: totalListenersCount ? ((activeListenersCount / totalListenersCount) * 100).toFixed(1) : 0,
    
    // 测验数据
    totalQuizzes: totalQuestionsInPresentation,
    totalAnswers: totalAnswersSubmitted,
    averageCorrectRate: typeof averageCorrectRate === 'string' ? 
                       averageCorrectRate.replace('%', '') : 
                       parseFloat(averageCorrectRate).toFixed(1),
    answersPerQuestion: totalQuestionsInPresentation > 0 ? 
                        (totalAnswersSubmitted / totalQuestionsInPresentation).toFixed(1) : 
                        0
  };
});

// 听众表现数据
const listenerPerformance = computed(() => {
  if (!presentationStats.value || !presentationStats.value.listener_performance) {
    return [];
  }
  return presentationStats.value.listener_performance;
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
    
    // 专门输出关键数据以便调试
    console.log('API返回的总听众数:', stats.total_listeners, '总参与者:', stats.total_participants);
    console.log('测验情况数据:', {
      '测验总数': stats.total_questions_in_presentation || stats.total_questions,
      '总答题数': stats.total_answers_submitted,
      '平均正确率': stats.average_correct_rate_across_all_questions || stats.average_correct_rate
    });
    
    if (stats && stats.listener_performance) {
      console.log('听众表现数据:', stats.listener_performance);
      console.log('活跃听众数量(listener_performance长度):', stats.listener_performance.length);
    } else {
      console.log('API返回中没有听众表现数据');
    }
    
    if (stats && stats.questions) {
      console.log('问题详情数据:', stats.questions.length ? `${stats.questions.length}个问题` : '无问题数据');
    }
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

.quiz-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
  border-bottom: 1px solid #eee;
  padding-bottom: 5px;
}

.quiz-item h4 {
  margin-top: 0;
  color: #333;
  margin-bottom: 0;
  flex: 1;
}

.quiz-status {
  padding: 4px 8px;
  border-radius: 12px;
  background-color: #f0f0f0;
  font-size: 12px;
  color: #777;
}

.quiz-status.high-response {
  background-color: #e3f5eb;
  color: #4dc189;
}

.quiz-item h5 {
  margin: 15px 0 10px;
  color: #555;
}

.high-rate {
  color: #4dc189 !important;
}

.medium-rate {
  color: #ff9900 !important;
}

.low-rate {
  color: #dc3545 !important;
}

.no-data-message {
  color: #999;
  font-style: italic;
  text-align: center;
  padding: 10px 0;
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

/* 听众表现表格 */
.listener-performance {
  margin-top: 30px;
}

.performance-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 15px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  overflow: hidden;
  border-radius: 8px;
}

.performance-table th, 
.performance-table td {
  padding: 12px 15px;
  text-align: left;
}

.performance-table thead {
  background-color: #4dc189;
  color: white;
}

.performance-table tr:nth-child(even) {
  background-color: #f9f9f9;
}

.performance-table tr:hover {
  background-color: #f0f9f6;
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
