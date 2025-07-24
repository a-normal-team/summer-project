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
      <button class="action-button generate-button" @click="generateQuiz" :disabled="loading">{{ loading ? '生成中...' : '基于所有文件生成随堂测验' }}</button>
      
      <div v-if="activeQuizzes.length > 0" class="active-quiz-section">
        <div class="section-header">
          <h3>当前活跃题目 ({{ activeQuizzes.length }}个):</h3>
          <button class="action-button danger" @click="deactivateAllQuizzes" :disabled="loading">
            停用所有活跃题目
          </button>
        </div>
        
        <div v-for="quiz in activeQuizzes" :key="quiz.id" class="quiz-item">
          <div class="question-content">
            <p class="question-text">{{ quiz.question_text }}</p>
            <div class="answer-options">
              <div v-for="(option, index) in quiz.options" :key="index" 
                   class="answer-option">
                <span class="option-label">{{ String.fromCharCode(65 + index) }}</span>
                <span class="option-text">
                  {{ option }}
                </span>
              </div>
            </div>
          </div>
          <div class="quiz-actions-row">
            <button class="action-button danger" @click="deactivateQuiz(quiz)" :disabled="loading">停用题目</button>
          </div>
          
          <div v-if="quiz.stats" class="quiz-stats">
            <h4>实时统计:</h4>
            <div class="stats-content">
              <div class="stat-row">
                <span class="stat-label">正确答案:</span>
                <span class="stat-value correct-answer">{{ quiz.correct_answer !== undefined ? getCorrectAnswerLabel(quiz) : '未知' }}</span>
              </div>
              <div class="stat-row">
                <span class="stat-label">总回答数:</span>
                <span class="stat-value">{{ quiz.stats.total_answers }}</span>
              </div>
              <div class="stat-row">
                <span class="stat-label">正确回答数:</span>
                <span class="stat-value">{{ quiz.stats.correct_answers }}</span>
              </div>
              <div class="stat-row">
                <span class="stat-label">正确率:</span>
                <span class="stat-value">{{ quiz.stats.correct_rate }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <div v-else class="empty-active-quiz">
        <p>当前没有活跃题目，请生成新题目</p>
      </div>
      
      <!-- 不再需要单独的所有题目列表，已经在当前活跃题目中显示了正确答案 -->
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
  getActiveQuestions,
  deactivateQuestion as apiDeactivateQuestion,
  getQuestionStats,
  generateQuestionsFromFile,
  generateQuestionsFromPresentation,
  getPresentationQuestions
} from '../../services/quiz';
import { getFilesByPresentation } from '../../services/file';

const router = useRouter();
const selectedPresentation = ref(null);
const selectedFile = ref(null);
const quizzes = ref([]);
const activeQuiz = ref(null); // 保留单个活跃问题的引用以兼容现有代码
const activeQuizzes = ref([]); // 存储所有活跃问题
const files = ref([]);
const presentationQuestions = ref([]);
const loading = ref(false);
const error = ref(null);

// 无需显示正确选项的功能

// 计算非活跃的测验题目
const inactiveQuizzes = computed(() => {
  return quizzes.value.filter(quiz => 
    !activeQuiz.value || quiz.id !== activeQuiz.value.id
  );
});

// 停用所有活跃题目
const deactivateAllQuizzes = async () => {
  if (!activeQuizzes.value || activeQuizzes.value.length === 0) return;
  
  if (confirm(`确定要停用所有活跃题目吗？`)) {
    loading.value = true;
    error.value = null;
    
    try {
      // 循环调用API停用所有活跃题目
      const deactivationPromises = activeQuizzes.value.map(quiz => apiDeactivateQuestion(quiz.id));
      await Promise.all(deactivationPromises);
      
      // 清空活跃题目列表
      activeQuizzes.value = [];
      activeQuiz.value = null;
      
      // 重新加载所有问题列表
      await loadPresentationQuestions(selectedPresentation.value.id);
    } catch (err) {
      console.error('停用所有题目失败:', err);
      error.value = err.message || '停用所有题目失败，请稍后再试';
    } finally {
      loading.value = false;
    }
  }
};

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
    
    // 获取该演讲的活跃题目
    await loadActiveQuestions(presentation.id);
    // 获取该演讲的所有问题
    await loadPresentationQuestions(presentation.id);
    
  } catch (err) {
    console.error('获取演讲详情失败:', err);
    error.value = err.message || '获取演讲详情失败，请稍后再试';
  } finally {
    loading.value = false;
  }
};

// 加载演讲的所有活跃题目
const loadActiveQuestions = async (presentationId) => {
  loading.value = true;
  
  try {
    // 获取所有活跃题目
    const activeQuestionsData = await getActiveQuestions(presentationId);
    console.log('从API获取的活跃题目数据:', activeQuestionsData);
    console.log('完整原始数据:', JSON.stringify(activeQuestionsData));
    
    // 清空现有的活跃题目列表
    activeQuizzes.value = [];
    
    // 检查数据结构，可能在active_questions字段下
    let questionsArray = activeQuestionsData;
    if (!Array.isArray(activeQuestionsData) && activeQuestionsData?.active_questions) {
      questionsArray = activeQuestionsData.active_questions;
      console.log('检测到数据在active_questions字段下');
    }
    
    // 如果有活跃题目，我们需要额外获取包含正确答案的完整题目信息
    if (Array.isArray(questionsArray) && questionsArray.length > 0) {
      // 首先获取所有题目（包括正确答案）
      const allQuestionsResponse = await getPresentationQuestions(presentationId);
      console.log('获取所有题目数据（包含正确答案）:', allQuestionsResponse);
      
      // 解析所有题目数据，提取出包含正确答案的完整题目列表
      let allQuestionsArray = [];
      if (Array.isArray(allQuestionsResponse)) {
        allQuestionsArray = allQuestionsResponse;
      } else if (allQuestionsResponse && Array.isArray(allQuestionsResponse.questions)) {
        allQuestionsArray = allQuestionsResponse.questions;
      } else if (allQuestionsResponse && typeof allQuestionsResponse === 'object') {
        allQuestionsArray = allQuestionsResponse.data || [];
      }
      
      // 创建ID到完整题目的映射，便于快速查找
      const questionsMap = {};
      for (const q of allQuestionsArray) {
        if (q.id) {
          questionsMap[q.id] = q;
        }
      }
      
      console.log('创建题目ID映射:', Object.keys(questionsMap));
      
      // 为每个活跃题目获取统计数据和正确答案
      for (const question of questionsArray) {
        try {
          // 验证问题对象是否包含必要的字段
          if (!question.id) {
            console.warn('活跃题目缺少ID:', question);
            continue;
          }

          // 确保有options字段
          if (!Array.isArray(question.options)) {
            console.warn(`题目ID(${question.id})缺少选项数组:`, question);
            question.options = [];
          }
          
          // 获取题目统计数据
          const stats = await getQuestionStats(question.id);
          question.stats = stats;
          
          // 从所有题目中查找匹配的题目以获取正确答案
          const fullQuestionInfo = questionsMap[question.id];
          if (fullQuestionInfo) {
            console.log(`找到题目(ID: ${question.id})的完整信息:`, fullQuestionInfo);
            
            // 从完整题目信息中复制正确答案
            if (fullQuestionInfo.correct_answer !== undefined) {
              question.correct_answer = fullQuestionInfo.correct_answer;
              console.log(`从完整信息中获取正确答案:`, question.correct_answer);
            } else {
              // 检查可能的替代字段
              const possibleFields = ['correct_option', 'correctAnswer', 'correct_option_index'];
              for (const field of possibleFields) {
                if (fullQuestionInfo[field] !== undefined) {
                  question.correct_answer = fullQuestionInfo[field];
                  console.log(`从完整信息的${field}字段获取正确答案:`, question.correct_answer);
                  break;
                }
              }
            }
          } else {
            console.log(`未找到题目(ID: ${question.id})的完整信息`);
            
            // 如果活跃题目本身有正确答案字段，就使用它
            if (question.correct_answer !== undefined) {
              console.log(`活跃题目已包含correct_answer字段:`, question.correct_answer);
            } else {
              // 检查可能的替代字段
              const possibleFields = ['correct_option', 'correctAnswer', 'correct_option_index'];
              for (const field of possibleFields) {
                if (question[field] !== undefined) {
                  question.correct_answer = question[field];
                  console.log(`从活跃题目的${field}字段获取正确答案:`, question.correct_answer);
                  break;
                }
              }
            }
          }
          
          console.log(`处理完成的活跃题目:`, {
            id: question.id,
            question_text: question.question_text,
            options: question.options,
            correct_answer: question.correct_answer,
            type: question.correct_answer !== undefined ? typeof question.correct_answer : 'undefined'
          });
        } catch (statsErr) {
          console.error(`获取题目(ID: ${question.id})统计失败:`, statsErr);
          question.stats = { total_answers: 0, correct_answers: 0, correct_rate: '0%' };
        }
        activeQuizzes.value.push(question);
      }
      
      // 保持与之前的代码兼容，保留第一个活跃题目在 activeQuiz 中
      activeQuiz.value = activeQuizzes.value[0];
    } else {
      // 没有活跃题目
      activeQuiz.value = null;
    }
  } catch (err) {
    console.error('获取活跃题目失败:', err);
    activeQuiz.value = null;
    activeQuizzes.value = [];
  } finally {
    loading.value = false;
  }
};

// 生成随堂测验
const generateQuiz = async () => {
  if (!selectedPresentation.value) {
    error.value = '请先选择一个演讲';
    return;
  }
  
  loading.value = true;
  error.value = null;
  
  try {
    // 使用新的API端点，基于演讲的所有上传文件生成题目
    const response = await generateQuestionsFromPresentation(selectedPresentation.value.id);
    console.log('基于演讲生成题目成功:', response);
    
    if (response && response.msg) {
      alert(response.msg);
      console.log('生成的问题ID列表:', response.question_ids);
    } else {
      alert('题目生成成功！');
    }
    
    // 重新加载活跃题目和所有题目
    await loadActiveQuestions(selectedPresentation.value.id);
    await loadPresentationQuestions(selectedPresentation.value.id);
  } catch (err) {
    console.error('基于演讲生成题目失败:', err);
    error.value = err.message || '生成题目失败，请稍后再试';
  } finally {
    loading.value = false;
  }
};

// 不再需要文件选择对话框，因为新的API端点会使用所有文件

// 获取正确答案对应的选项字母
const getCorrectAnswerLabel = (quiz) => {
  console.log('正确答案数据:', quiz?.correct_answer, '类型:', typeof quiz?.correct_answer);
  
  if (!quiz || !Array.isArray(quiz.options)) {
    return '未知';
  }
  
  // 正确答案可能是数字索引或字符串内容或空值
  if (quiz.correct_answer === undefined || quiz.correct_answer === null) {
    return '未知';
  }
  
  let index = -1;
  
  if (typeof quiz.correct_answer === 'number') {
    // 如果是数字索引（0, 1, 2, 3等）
    index = quiz.correct_answer;
    console.log('正确答案是数字索引:', index);
  } else if (typeof quiz.correct_answer === 'string') {
    // 如果是字符串，可能是选项内容或字母(A,B,C,D)
    if (quiz.correct_answer.length === 1 && /[A-Z]/i.test(quiz.correct_answer)) {
      // 如果是单个字母，转换为索引 (A->0, B->1, etc.)
      index = quiz.correct_answer.toUpperCase().charCodeAt(0) - 65;
      console.log('正确答案是字母:', quiz.correct_answer, '转为索引:', index);
    } else {
      // 如果是选项内容字符串，查找匹配的选项
      index = quiz.options.findIndex(option => 
        option.toLowerCase() === quiz.correct_answer.toLowerCase()
      );
      console.log('正确答案是选项内容，查找结果索引:', index);
    }
  }
  
  // 验证索引是否在有效范围内
  if (index >= 0 && index < quiz.options.length) {
    const result = String.fromCharCode(65 + index);
    console.log('返回的正确答案字母:', result);
    return result;
  } else {
    console.log('索引超出范围或未找到匹配项:', index);
    return '未知';
  }
};

// 停用指定题目
const deactivateQuiz = async (quiz) => {
  if (!quiz) return;
  
  if (confirm(`确定要停用题目"${quiz.question_text}"吗？`)) {
    loading.value = true;
    error.value = null;
    
    try {
      // 调用API停用题目
      await apiDeactivateQuestion(quiz.id);
      
      // 从活跃题目列表中移除该题目
      activeQuizzes.value = activeQuizzes.value.filter(q => q.id !== quiz.id);
      
      // 如果停用的是当前引用的活跃题目，则更新或重置
      if (activeQuiz.value && activeQuiz.value.id === quiz.id) {
        activeQuiz.value = activeQuizzes.value.length > 0 ? activeQuizzes.value[0] : null;
      }
      
      // 重新加载所有问题列表
      await loadPresentationQuestions(selectedPresentation.value.id);
    } catch (err) {
      console.error('停用题目失败:', err);
      error.value = err.message || '停用题目失败，请稍后再试';
    } finally {
      loading.value = false;
    }
  }
};

// 加载演讲的所有问题
const loadPresentationQuestions = async (presentationId) => {
  loading.value = true;
  
  try {
    const response = await getPresentationQuestions(presentationId);
    console.log('从API获取的所有题目响应:', response);
    console.log('所有题目原始响应结构:', JSON.stringify(response).substring(0, 500) + '...');
    
    // 处理不同格式的API响应
    let questions = [];
    if (Array.isArray(response)) {
      questions = response;
      console.log('响应是数组格式');
    } else if (response && Array.isArray(response.questions)) {
      questions = response.questions;
      console.log('响应是包含questions数组的对象');
    } else if (response && typeof response === 'object') {
      questions = response.data || [];
      console.log('响应是包含data的对象');
    }
    
    console.log('解析后的问题数量:', questions.length);
    
    if (questions.length > 0) {
      // 验证并处理每个问题
      questions.forEach(question => {
        // 确保有options字段
        if (!Array.isArray(question.options)) {
          console.warn(`题目ID(${question.id})缺少选项数组:`, question);
          question.options = [];
        }
        
        // 处理正确答案字段，考虑不同命名可能
        console.log('题目数据中的所有字段:', Object.keys(question));
        
        // 检查可能的正确答案字段名
        if (question.correct_answer === undefined) {
          const possibleFields = ['correct_option', 'correctAnswer', 'correct_option_index'];
          for (const field of possibleFields) {
            if (question[field] !== undefined) {
              console.log(`找到替代正确答案字段 ${field}:`, question[field]);
              question.correct_answer = question[field];
              break;
            }
          }
        }
        
        console.log(`处理的题目:`, {
          id: question.id,
          question_text: question.question_text,
          options: question.options.length,
          correct_answer: question.correct_answer,
          type: question.correct_answer !== undefined ? typeof question.correct_answer : 'undefined'
        });
      });
      
      presentationQuestions.value = questions;
    } else {
      console.log('没有找到演讲的题目');
      presentationQuestions.value = [];
    }
  } catch (err) {
    console.error('获取演讲所有题目失败:', err);
    presentationQuestions.value = [];
  } finally {
    loading.value = false;
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

.action-button.danger {
  background-color: #e74c3c;
}

.action-button.danger:hover {
  background-color: #c0392b;
}

.action-button.danger:disabled {
  background-color: #f5b8b2;
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
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 15px;
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
  margin-bottom: 20px; /* 增加底部间距 */
  border-left: 4px solid #4dc189; /* 添加左侧边框 */
}

.active-quiz-section .quiz-item {
  border-left: 4px solid #4dc189; /* 活跃题目使用绿色边框，与其他页面保持一致 */
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

.all-questions-section {
  margin-top: 30px;
  padding: 15px;
  background-color: #f8f9fa;
  border-radius: 8px;
}

.all-questions-section h3 {
  margin-bottom: 15px;
  color: #4a4a4a;
}

.questions-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
  max-height: 500px;
  overflow-y: auto;
}

.answer-text {
  font-weight: bold;
  color: #4dc189;
  margin-top: 5px;
}

/* ABCD样式选项 */
.answer-options {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  margin: 0.5rem 0;
  padding: 0 1rem;
}

.answer-option {
  display: flex;
  align-items: center;
  padding: 0.75rem 1rem;
  border-radius: 8px;
  background: #f5f5f5;
  position: relative;
  border: 1px solid transparent;
}

.answer-option:hover {
  background: #f0f9f6;
  border-color: #4dc189;
}

.option-label {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 2rem;
  height: 2rem;
  border-radius: 50%;
  background: #e0e0e0;
  margin-right: 1rem;
  font-weight: 500;
  flex-shrink: 0;
}

.option-text {
  flex: 1;
  font-size: 1rem;
}

/* 正确选项样式已移除 */

.quiz-actions-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: 10px;
  margin-bottom: 10px;
}

.correct-answer {
  color: #4dc189;
  font-weight: bold;
}

/* 正确答案文本样式已移除 */
</style>
