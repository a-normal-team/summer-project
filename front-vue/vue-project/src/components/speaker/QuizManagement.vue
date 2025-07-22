<template>
  <div class="sub-dashboard-section">
    <h2>题目管理</h2>
    <div v-if="loading" class="loading-state">
      <p>加载中...</p>
    </div>
    <div v-else-if="error" class="error-state">
      <p>{{ error }}</p>
      <button @click="checkSelectedPresentation" class="retry-button">重试</button>
    </div>
    <div v-else-if="!selectedPresentation" class="no-selection">
      <p>请先选择一个演讲</p>
      <router-link to="/speaker/dashboard/presentations" class="nav-link">选择演讲</router-link>
    </div>
    <div v-else>
      <div class="presentation-info">
        <h3>当前选中: {{ selectedPresentation.title }}</h3>
        <p>{{ selectedPresentation.description }}</p>
      </div>
      <button class="action-button generate-button" @click="generateQuiz" :disabled="loading">生成随堂测验</button>
      
      <div v-if="activeQuiz" class="active-quiz-section">
        <h3>当前活跃题目:</h3>
        <div class="quiz-item">
          <div class="question-content">
            <p class="question-text">{{ activeQuiz.question_text }}</p>
            <p class="options-text">选项: {{ activeQuiz.options.join(', ') }}</p>
          </div>
          <button class="action-button danger" @click="deactivateQuiz" :disabled="loading">停用题目</button>
        </div>
        
        <div v-if="activeQuiz.stats" class="quiz-stats">
          <h4>实时统计:</h4>
          <div class="stats-content">
            <div class="stat-row">
              <span class="stat-label">总回答数:</span>
              <span class="stat-value">{{ activeQuiz.stats.total_answers }}</span>
            </div>
            <div class="stat-row">
              <span class="stat-label">正确回答数:</span>
              <span class="stat-value">{{ activeQuiz.stats.correct_answers }}</span>
            </div>
            <div class="stat-row">
              <span class="stat-label">正确率:</span>
              <span class="stat-value">{{ activeQuiz.stats.correct_rate }}</span>
            </div>
          </div>
        </div>
      </div>
      
      <div v-else class="empty-active-quiz">
        <p>当前没有活跃题目，请生成新题目</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRouter } from 'vue-router';
import { getPresentationById } from '../../services/presentation';
import { 
  createQuestion, 
  getActiveQuestion, 
  deactivateQuestion as apiDeactivateQuestion,
  getQuestionStats
} from '../../services/quiz';
import { getFilesByPresentation } from '../../services/file';

const router = useRouter();
const selectedPresentation = ref(null);
const selectedFile = ref(null);
const quizzes = ref([]);
const activeQuiz = ref(null);
const files = ref([]);
const loading = ref(false);
const error = ref(null);

// 计算非活跃的测验题目
const inactiveQuizzes = computed(() => {
  return quizzes.value.filter(quiz => 
    !activeQuiz.value || quiz.id !== activeQuiz.value.id
  );
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
    
    // 获取演讲的文件，用于从文件生成题目
    const filesList = await getFilesByPresentation(presentation.id);
    files.value = filesList || [];
    
    // 获取该演讲的题目
    await loadActiveQuestion(presentation.id);
    // 注意：API文档中没有获取所有题目的端点，所以这里我们只能获取当前活跃题目
    
  } catch (err) {
    console.error('获取演讲详情失败:', err);
    error.value = err.message || '获取演讲详情失败，请稍后再试';
  } finally {
    loading.value = false;
  }
};

// 加载演讲的活跃题目
const loadActiveQuestion = async (presentationId) => {
  loading.value = true;
  
  try {
    const activeQuestionData = await getActiveQuestion(presentationId);
    // 如果有活跃题目
    if (activeQuestionData && !activeQuestionData.msg) {
      activeQuiz.value = activeQuestionData;
      
      // 获取题目统计
      const stats = await getQuestionStats(activeQuestionData.id);
      activeQuiz.value.stats = stats;
    } else {
      activeQuiz.value = null;
    }
  } catch (err) {
    console.error('获取活跃题目失败:', err);
    activeQuiz.value = null;
  } finally {
    loading.value = false;
  }
};

// 生成随堂测验
const generateQuiz = async () => {
  if (!selectedPresentation.value) return;
  
  loading.value = true;
  error.value = null;
  
  const quizData = {
    question_text: "Spring Boot 主要用于什么?",
    question_type: "multiple_choice",
    options: ["创建独立的Spring应用", "数据库管理", "前端开发", "操作系统开发"],
    correct_answer: "创建独立的Spring应用"
  };
  
  try {
    // 调用API创建题目
    const response = await createQuestion(selectedPresentation.value.id, quizData);
    console.log('题目创建成功:', response);
    
    // 重新加载活跃题目
    await loadActiveQuestion(selectedPresentation.value.id);
  } catch (err) {
    console.error('创建题目失败:', err);
    error.value = err.message || '创建题目失败，请稍后再试';
  } finally {
    loading.value = false;
  }
};

// 停用当前题目
const deactivateQuiz = async () => {
  if (!activeQuiz.value) return;
  
  if (confirm('确定要停用当前题目吗？')) {
    loading.value = true;
    error.value = null;
    
    try {
      // 调用API停用题目
      await apiDeactivateQuestion(activeQuiz.value.id);
      
      // 重置活跃题目
      activeQuiz.value = null;
    } catch (err) {
      console.error('停用题目失败:', err);
      error.value = err.message || '停用题目失败，请稍后再试';
    } finally {
      loading.value = false;
    }
  }
};

// 删除题目（注意：API文档中没有删除题目的端点，这里保留为占位符）
const deleteQuiz = (quiz) => {
  alert(`API中没有提供删除题目的功能: ${quiz.question_text}`);
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

.generate-button {
  margin-bottom: 20px;
  width: auto;
}

.quiz-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.no-selection, .empty-quizzes, .empty-active-quiz, .loading-state, .error-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 30px 0;
}

.nav-link, .retry-button {
  margin-top: 15px;
  text-decoration: none;
  background-color: #4dc189;
  color: white;
  padding: 10px 20px;
  border-radius: 20px;
  font-weight: bold;
  transition: all 0.3s ease;
  border: none;
  cursor: pointer;
}

.nav-link:hover, .retry-button:hover {
  background-color: #3aa875;
  transform: translateY(-1px);
}

.error-state {
  color: #e74c3c;
}

.action-button:disabled {
  background-color: #a8d9c6;
  cursor: not-allowed;
  transform: none;
}

.quiz-stats {
  margin-top: 20px;
  background-color: #f0f9f6;
  border-radius: 8px;
  padding: 15px;
}

.quiz-stats h4 {
  margin-top: 0;
  color: #333;
  margin-bottom: 10px;
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

.active-quiz-section {
  background-color: #f0f9f6;
  border: 2px solid #4dc189;
  border-radius: 8px;
  padding: 15px;
  margin-bottom: 20px;
}

.question-content {
  margin-bottom: 10px;
}

.question-text {
  font-weight: bold;
  font-size: 16px;
  margin-bottom: 5px;
}

.options-text, .answer-text {
  font-size: 14px;
  color: #555;
}

.answer-text {
  font-weight: bold;
  color: #4dc189;
}

.quiz-actions {
  display: flex;
  gap: 10px;
  margin-top: 10px;
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
