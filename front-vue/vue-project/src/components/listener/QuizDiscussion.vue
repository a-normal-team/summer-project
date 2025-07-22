<template>
  <div class="quiz-discussion-container sub-dashboard-section">
    <h2 class="section-title">测验讨论区 (演讲ID: {{ presentationId }})</h2>
    
    <div v-if="loading" class="loading-spinner">
      <p>正在加载测验题目...</p>
    </div>
    
    <div v-else-if="error" class="error-message">
      <p>{{ error }}</p>
      <button class="action-button" @click="fetchPresentationQuestions">重试</button>
    </div>
    
    <div v-else-if="questions.length === 0" class="empty-state">
      <p>当前演讲暂无测验题目</p>
    </div>
    
    <div v-else class="questions-list">
      <div v-for="question in questions" :key="question.id" class="question-card">
        <div class="question-header">
          <h3>{{ question.question_text }}</h3>
          <span class="question-status" :class="question.is_active ? 'active' : 'inactive'">
            {{ question.is_active ? '进行中' : '已结束' }}
          </span>
        </div>
        
        <div class="question-options" v-if="question.question_type === 'multiple_choice'">
          <div 
            v-for="(option, index) in question.options" 
            :key="index" 
            class="option-item"
          >
            <span class="option-label">{{ getOptionLabel(index) }}</span>
            <span class="option-text">{{ option }}</span>
          </div>
        </div>
        
        <div class="question-stats" v-if="!question.is_active">
          <div class="stats-item">
            <span class="label">总回答人数:</span>
            <span class="value">{{ question.stats?.total_answers || 0 }}</span>
          </div>
          <div class="stats-item">
            <span class="label">正确率:</span>
            <span class="value">{{ question.stats?.correct_rate || '0%' }}</span>
          </div>
        </div>
        
        <div v-if="!question.is_active && question.showDiscussion" class="question-discussion">
          <h4>讨论区</h4>
          
          <div v-if="question.loadingComments" class="loading-comments">
            加载评论中...
          </div>
          
          <div v-else class="discussion-area-wrapper">
            <DiscussionArea 
              :comments="question.comments || []" 
              :currentUser="currentUser"
              :isLoggedIn="isLoggedIn"
              @submit="(comment) => submitComment(question.id, comment)"
              @reply="(comment, parentId) => replyComment(question.id, comment, parentId)"
            />
          </div>
        </div>
        
        <div class="question-actions" v-if="!question.is_active && !question.showDiscussion">
          <button class="action-button" @click="toggleDiscussion(question)">
            查看讨论
          </button>
        </div>
        
        <div class="question-actions" v-if="!question.is_active && question.showDiscussion">
          <button class="action-button secondary" @click="toggleDiscussion(question)">
            隐藏讨论
          </button>
        </div>
        
        <div v-if="question.is_active" class="question-answer-section">
          <div class="answer-options-compact">
            <div 
              v-for="(option, index) in question.options" 
              :key="index"
              class="answer-option-compact"
              :class="{
                'selected': selectedAnswers[question.id] === index,
                'disabled': answerResults[question.id]?.success,
                'correct-answer': answerResults[question.id]?.success && answerResults[question.id]?.correctAnswer === index
              }"
              @click="answerResults[question.id]?.success ? null : selectAnswer(question.id, index)"
            >
              {{ getOptionLabel(index) }}
              <span 
                v-if="answerResults[question.id]?.success && answerResults[question.id]?.correctAnswer === index" 
                class="correct-mark-compact">✓</span>
            </div>
          </div>
          
          <div v-if="answerResults[question.id]?.error" class="answer-error">
            {{ answerResults[question.id].message }}
          </div>
          
          <div v-if="answerResults[question.id]?.success" class="answer-result" :class="{'correct': answerResults[question.id].correct}">
            {{ answerResults[question.id].message }}
          </div>
          
          <div class="answer-actions" v-if="!answerResults[question.id]?.success">
            <button 
              class="action-button" 
              @click="submitQuestionAnswer(question)"
              :disabled="submittingAnswer || selectedAnswers[question.id] === undefined"
            >
              {{ submittingAnswer ? '提交中...' : '提交答案' }}
            </button>
          </div>
          
          <div class="question-notice">
            <p>题目讨论将在该题结束后开放</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, inject, computed, watch } from 'vue';
import { useRoute } from 'vue-router';
import { getActiveQuestion, submitAnswer } from '../../services/quiz';
import { getComments, addComment } from '../../services/discussion';
import DiscussionArea from '../common/DiscussionArea.vue';

const route = useRoute();
// 从父组件 ListenerDashboard 获取选中的演讲ID
const selectedPresentationId = inject('selectedPresentationId', ref(null));
// 也兼容路由参数方式
const presentationId = computed(() => route.params.id || selectedPresentationId.value);

const questions = ref([]);
const loading = ref(true);
const error = ref('');
const selectedAnswers = ref({}); // 存储用户选择的答案 {questionId: selectedOption}
const submittingAnswer = ref(false); // 控制提交答案按钮的加载状态
const answerResults = ref({}); // 存储答案提交结果 {questionId: {correct: boolean, message: string}}

// 模拟当前用户数据，实际项目中应该从全局状态或服务中获取
const currentUser = reactive({
  id: 1,
  username: 'currentUser',
  role: 'listener'
});

const isLoggedIn = ref(true);

// 获取演讲的所有测验题目
const fetchPresentationQuestions = async () => {
  loading.value = true;
  error.value = '';
  
  // 首先检查presentationId是否有效
  if (!presentationId.value || presentationId.value === 'undefined') {
    console.error('无效的演讲ID');
    error.value = '无效的演讲ID，请返回选择有效的演讲';
    loading.value = false;
    return;
  }
  
  try {
    let activeQuestion = null;
    
    // 尝试获取活跃题目，如果API未准备好或出错，不阻止整个组件渲染
    try {
      console.log(`正在获取演讲ID ${presentationId.value} 的活跃题目`);
      activeQuestion = await getActiveQuestion(presentationId.value);
    } catch (activeErr) {
      console.warn(`获取演讲ID ${presentationId.value} 的活跃题目失败`, activeErr);
    }
    
    // 初始化一个空的问题列表
    const questionsList = [];
    
    // 如果有活跃题目，将其添加到问题列表
    if (activeQuestion && !activeQuestion.msg) {
      activeQuestion.is_active = true;
      activeQuestion.comments = [];
      activeQuestion.showDiscussion = false;
      activeQuestion.loadingComments = false;
      questionsList.push(activeQuestion);
    }
    
    // 这里应该添加获取演讲的历史题目的API调用
    // 例如：const historyQuestions = await getPresentationHistoryQuestions(presentationId.value);
    // 并将结果添加到 questionsList 中
    
    questions.value = questionsList;
    
    // 如果问题列表为空，可以在这里设置一个提示信息
    if (questions.value.length === 0) {
      console.log('当前演讲暂无测验题目');
    }
    
  } catch (err) {
    console.error('获取演讲题目失败:', err);
    error.value = '获取演讲题目失败，请稍后重试';
  } finally {
    loading.value = false;
  }
};

// 获取题目的评论
const fetchQuestionComments = async (question) => {
  if (question.is_active) return; // 活跃题目不加载评论
  
  question.loadingComments = true;
  
  try {
    // 尝试获取评论，如果API未准备好，使用空数组
    try {
      const comments = await getComments(question.id);
      
      // 检查是否为错误消息
      if (comments && comments.msg === "Discussion is only available after question is deactivated") {
        console.warn(`题目(ID: ${question.id})尚未停用，不能查看讨论`);
        question.comments = [];
      } else {
        // 根据API文档返回的是数组格式的评论列表
        question.comments = Array.isArray(comments) ? comments : [];
      }
    } catch (commentsErr) {
      console.warn(`获取题目(ID: ${question.id})评论失败，使用空评论列表`, commentsErr);
      // 设置空评论列表，以便UI正常显示
      question.comments = [];
    }
  } catch (err) {
    console.error('获取题目评论失败:', err);
    // 保留原有评论，如果有的话
    question.comments = question.comments || [];
  } finally {
    question.loadingComments = false;
  }
};

// 提交新评论
const submitComment = async (questionId, commentText) => {
  if (!commentText.trim()) return;
  
  const question = questions.value.find(q => q.id === questionId);
  if (!question || question.is_active) return;
  
  try {
    // 按照API文档，发送评论
    const response = await addComment(questionId, { 
      commentText: commentText 
    });
    
    if (response && response.msg === "Comment added successfully") {
      console.log(`评论添加成功，评论ID: ${response.comment_id}`);
      // 重新加载评论
      await fetchQuestionComments(question);
    } else if (response && response.msg === "Discussion is only available after question is deactivated") {
      console.warn('题目尚未停用，不能添加评论');
      // 可以添加用户提示
    }
  } catch (err) {
    console.error('提交评论失败:', err);
    // 可以添加错误提示
  }
};

// 回复评论
const replyComment = async (questionId, commentText, parentCommentId) => {
  if (!commentText.trim() || !parentCommentId) return;
  
  const question = questions.value.find(q => q.id === questionId);
  if (!question || question.is_active) return;
  
  try {
    // 按照API文档，发送回复评论请求
    const response = await addComment(questionId, {
      commentText: commentText,
      parentCommentId: parentCommentId
    });
    
    if (response && response.msg === "Comment added successfully") {
      console.log(`回复评论添加成功，评论ID: ${response.comment_id}`);
      // 重新加载评论
      await fetchQuestionComments(question);
    } else if (response && response.msg === "Discussion is only available after question is deactivated") {
      console.warn('题目尚未停用，不能添加回复');
      // 可以添加用户提示
    }
  } catch (err) {
    console.error('回复评论失败:', err);
    // 可以添加错误提示
  }
};

// 切换讨论区显示状态
const toggleDiscussion = async (question) => {
  question.showDiscussion = !question.showDiscussion;
  
  // 首次显示讨论区时加载评论
  if (question.showDiscussion && !question.comments.length) {
    await fetchQuestionComments(question);
  }
};

// 获取选项标签 (A, B, C, D...)
const getOptionLabel = (index) => {
  return String.fromCharCode(65 + index); // A=65, B=66, ...
};

// 用户选择答案选项
const selectAnswer = (questionId, optionIndex) => {
  selectedAnswers.value = {
    ...selectedAnswers.value,
    [questionId]: optionIndex
  };
};

// 提交问题答案
const submitQuestionAnswer = async (question) => {
  if (!question || !question.is_active) return;
  
  const selectedOption = selectedAnswers.value[question.id];
  // 如果用户未选择任何选项
  if (selectedOption === undefined) {
    answerResults.value = {
      ...answerResults.value,
      [question.id]: {
        error: true,
        message: '请选择一个答案'
      }
    };
    return;
  }
  
  submittingAnswer.value = true;
  
  try {
    // 提交答案到API
    const result = await submitAnswer(question.id, selectedOption);
    console.log('提交答案结果:', result);
    
    // 处理返回结果
    if (result && result.msg === "Answer submitted successfully") {
      answerResults.value = {
        ...answerResults.value,
        [question.id]: {
          success: true,
          correct: result.correct || false,
          message: result.correct ? '回答正确！' : '回答错误。',
          correctAnswer: result.correct_answer
        }
      };
      
      // 重新获取题目状态，因为回答后可能状态会变化
      setTimeout(() => {
        fetchPresentationQuestions();
      }, 2000);
    } else {
      answerResults.value = {
        ...answerResults.value,
        [question.id]: {
          error: true,
          message: result.msg || '提交答案失败'
        }
      };
    }
  } catch (err) {
    console.error('提交答案失败:', err);
    answerResults.value = {
      ...answerResults.value,
      [question.id]: {
        error: true,
        message: '提交答案时发生错误，请稍后重试'
      }
    };
  } finally {
    submittingAnswer.value = false;
  }
};

// 重置问题答案状态
const resetAnswerState = (questionId) => {
  // 删除该问题的选择和结果
  const newSelectedAnswers = { ...selectedAnswers.value };
  delete newSelectedAnswers[questionId];
  selectedAnswers.value = newSelectedAnswers;
  
  const newAnswerResults = { ...answerResults.value };
  delete newAnswerResults[questionId];
  answerResults.value = newAnswerResults;
};

// 监听演讲ID变化
watch(presentationId, (newId, oldId) => {
  if (newId && newId !== oldId) {
    console.log(`演讲ID变更为: ${newId}`);
    fetchPresentationQuestions();
  }
});

onMounted(() => {
  fetchPresentationQuestions();
});
</script>

<style scoped>
.quiz-discussion-container {
  padding: 1.5rem;
  width: 100%; /* 确保容器占据父元素的全部宽度 */
  box-sizing: border-box; /* 确保padding不会导致宽度溢出 */
}

.section-title {
  margin-bottom: 1.5rem;
  font-size: 1.75rem;
  font-weight: 600;
  color: #333;
}

.loading-spinner,
.empty-state,
.error-message {
  text-align: center;
  padding: 2rem;
  color: #666;
  background: #f9f9f9;
  border-radius: 8px;
}

.error-message {
  color: #d32f2f;
}

.questions-list {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  width: 100%; /* 确保列表占据全部宽度 */
}

.question-card {
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  width: 100%; /* 确保卡片占据容器的全部宽度 */
}

.question-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 1.5rem;
  border-bottom: 1px solid #eee;
}

.question-header h3 {
  font-size: 1.2rem;
  font-weight: 500;
  margin: 0;
  flex: 1;
}

.question-status {
  font-size: 0.875rem;
  padding: 0.25rem 0.75rem;
  border-radius: 1rem;
  font-weight: 500;
}

.question-status.active {
  background: #e3f2fd;
  color: #1976d2;
}

.question-status.inactive {
  background: #e8eaed;
  color: #5f6368;
}

.question-options {
  padding: 1rem 1.5rem;
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 0.75rem;
}

.option-item {
  display: flex;
  align-items: center;
  padding: 0.5rem;
  background: #f5f5f5;
  border-radius: 4px;
}

.option-label {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 1.75rem;
  height: 1.75rem;
  border-radius: 50%;
  background: #e0e0e0;
  margin-right: 0.75rem;
  font-weight: 500;
}

.question-stats {
  padding: 0.75rem 1.5rem;
  background: #f9f9f9;
  display: flex;
  gap: 2rem;
}

.stats-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.stats-item .label {
  color: #666;
}

.stats-item .value {
  font-weight: 500;
  color: #333;
}

.question-discussion {
  padding: 1rem 1.5rem;
  border-top: 1px solid #eee;
  width: 100%;
  min-height: 300px;
  display: flex;
  flex-direction: column;
}

.question-discussion h4 {
  margin-top: 0;
  margin-bottom: 1rem;
  font-size: 1.1rem;
  font-weight: 500;
}

.question-actions {
  padding: 1rem 1.5rem;
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  border-top: 1px solid #eee;
}

.action-button {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 4px;
  background: #1976d2;
  color: white;
  font-weight: 500;
  cursor: pointer;
  transition: background 0.2s;
}

.action-button:hover {
  background: #1565c0;
}

.action-button.secondary {
  background: #e0e0e0;
  color: #333;
}

.action-button.secondary:hover {
  background: #d5d5d5;
}

.question-notice {
  padding: 0.75rem 1.5rem;
  background: #fff8e1;
  color: #ff8f00;
  font-size: 0.875rem;
  text-align: center;
}

.loading-comments {
  text-align: center;
  padding: 1rem;
  color: #666;
}

.discussion-area-wrapper {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-height: 250px;
  width: 100%; /* 确保讨论区包装器占据全部宽度 */
}

.discussion-area-wrapper :deep(.discussion-area) {
  flex: 1;
  display: flex;
  flex-direction: column;
  width: 100%; /* 确保讨论区占据全部宽度 */
}

.discussion-area-wrapper :deep(.comments-list) {
  flex: 1;
  overflow-y: auto;
  max-height: 400px;
  width: 100%; /* 确保评论列表占据全部宽度 */
}

.discussion-area-wrapper :deep(.comment-input-area) {
  margin-top: auto;
}

/* 添加问题回答相关样式 */
.question-answer-section {
  padding: 1rem 1.5rem;
  border-top: 1px solid #eee;
}

.answer-options-compact {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.answer-option-compact {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 3rem;
  height: 3rem;
  border-radius: 50%;
  background: #f5f5f5;
  cursor: pointer;
  transition: all 0.2s;
  position: relative;
  font-weight: 500;
  font-size: 1.1rem;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

.answer-option-compact:hover {
  background: #e3f2fd;
  transform: translateY(-2px);
  box-shadow: 0 3px 6px rgba(0,0,0,0.1);
}

.answer-option-compact.selected {
  background: #1976d2;
  color: white;
  box-shadow: 0 2px 5px rgba(25, 118, 210, 0.3);
}

.answer-option-compact.disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.answer-option-compact.correct-answer {
  background: #4caf50;
  color: white;
}

.correct-mark-compact {
  position: absolute;
  bottom: -0.5rem;
  right: -0.5rem;
  width: 1.5rem;
  height: 1.5rem;
  display: flex;
  justify-content: center;
  align-items: center;
  background: white;
  border-radius: 50%;
  color: #4caf50;
  font-size: 1rem;
  font-weight: bold;
  box-shadow: 0 1px 2px rgba(0,0,0,0.2);
}

.answer-error {
  padding: 0.5rem 0.75rem;
  background: #ffebee;
  color: #d32f2f;
  border-radius: 4px;
  margin-bottom: 1rem;
  font-size: 0.875rem;
}

.answer-result {
  padding: 0.5rem 0.75rem;
  background: #ffebee;
  color: #d32f2f;
  border-radius: 4px;
  margin-bottom: 1rem;
  font-size: 0.875rem;
}

.answer-result.correct {
  background: #e8f5e9;
  color: #2e7d32;
}

.answer-actions {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 1rem;
}
</style>
