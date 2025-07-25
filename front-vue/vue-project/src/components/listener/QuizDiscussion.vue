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
      <div 
        v-for="question in questions" 
        :key="question.id" 
        class="question-card"
        :data-question-id="question.id"
        :class="{'current-question': currentQuestionId === question.id}"
      >
        <div class="question-header">
          <h3>{{ question.question_text }}</h3>
          <span class="question-status" :class="question.is_active ? 'active' : 'inactive'">
            {{ question.is_active ? '进行中' : '已结束' }}
          </span>
        </div>
        
        <div class="answer-options" v-if="question.question_type === 'multiple_choice'">
          <div 
            v-for="(option, index) in question.options" 
            :key="index" 
            class="answer-option"
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
        
        <div v-if="question.showDiscussion" class="question-discussion">
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
              @reply="(comment) => console.log('切换回复状态:', comment.id)"
            />
          </div>
        </div>
        
        <!-- 所有题目都可以查看讨论 -->
        <div class="question-actions" v-if="!question.showDiscussion">
          <button class="action-button" @click="toggleDiscussion(question)">
            查看讨论
          </button>
        </div>
        
        <div class="question-actions" v-if="question.showDiscussion">
          <button class="action-button secondary" @click="toggleDiscussion(question)">
            隐藏讨论
          </button>
        </div>
        
        <div v-if="question.is_active" class="question-answer-section">
          <!-- 已回答状态展示 -->
          <div v-if="question.hasAnswered || answerResults[question.id]?.success" class="question-answered">
            <div class="answer-options answer-options-simple">
              <div 
                v-for="(option, index) in question.options" 
                :key="index"
                class="answer-option answer-option-simple"
                :class="{
                  'selected': selectedAnswers[question.id] === index,
                  'disabled': true,
                  'correct-answer': answerResults[question.id]?.correctAnswer === index
                }"
              >
                <span class="option-label">{{ getOptionLabel(index) }}</span>
                <span 
                  v-if="answerResults[question.id]?.correctAnswer === index" 
                  class="correct-text">正确</span>
              </div>
            </div>
            
            <div v-if="answerResults[question.id]?.success" class="answer-result" :class="{'correct': answerResults[question.id].correct}">
              {{ answerResults[question.id].message }}
            </div>
            
            <div class="already-answered-notice">
              <p>您已回答过此题</p>
            </div>
          </div>
          
          <!-- 未回答状态展示 -->
          <div v-else>
            <div class="answer-options answer-options-simple">
              <div 
                v-for="(option, index) in question.options" 
                :key="index"
                class="answer-option answer-option-simple"
                :class="{
                  'selected': selectedAnswers[question.id] === index
                }"
                @click="selectAnswer(question.id, index)"
              >
                <span class="option-label">{{ getOptionLabel(index) }}</span>
              </div>
            </div>
            
            <div v-if="answerResults[question.id]?.error" class="answer-error">
              {{ answerResults[question.id].message }}
            </div>
            
            <div class="answer-actions">
              <button 
                class="action-button" 
                @click="submitQuestionAnswer(question)"
                :disabled="submittingAnswer || selectedAnswers[question.id] === undefined"
              >
                {{ submittingAnswer ? '提交中...' : '提交答案' }}
              </button>
            </div>
          </div>
          
          <!-- 已移除限制提示，所有题目都可以讨论 -->
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, inject, computed, watch } from 'vue';
import { useRoute } from 'vue-router';
import { getActiveQuestion, getActiveQuestions, submitAnswer, getPresentationQuestions } from '../../services/quiz';
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
// 添加当前活跃问题的ID引用，用于记住用户当前查看的问题
const currentQuestionId = ref(null);
// 使用函数从localStorage加载数据，确保数据持久化
const loadSelectedAnswers = () => {
  const savedAnswers = localStorage.getItem(`quiz_selected_answers_${presentationId.value}`);
  return savedAnswers ? JSON.parse(savedAnswers) : {};
};
const loadAnswerResults = () => {
  const savedResults = localStorage.getItem(`quiz_answer_results_${presentationId.value}`);
  return savedResults ? JSON.parse(savedResults) : {};
};
const selectedAnswers = ref(loadSelectedAnswers()); // 存储用户选择的答案 {questionId: selectedOption}
const submittingAnswer = ref(false); // 控制提交答案按钮的加载状态
const answerResults = ref(loadAnswerResults()); // 存储答案提交结果 {questionId: {correct: boolean, message: string}}

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
    // 确保已加载当前演讲的已保存答案和结果
    if (presentationId.value) {
      reloadSavedAnswersAndResults(presentationId.value);
    }
    
    // 初始化一个空的问题列表
    const questionsList = [];
    
    // 尝试获取所有活跃题目，如果API未准备好或出错，不阻止整个组件渲染
    try {
      console.log(`正在获取演讲ID ${presentationId.value} 的所有活跃题目`);
      const activeQuestions = await getActiveQuestions(presentationId.value);
      console.log('获取到的活跃题目:', activeQuestions); // 添加日志，查看处理后的数据
      
      if (Array.isArray(activeQuestions) && activeQuestions.length > 0) {
        // 将所有活跃题目添加到问题列表
        for (const question of activeQuestions) {
          question.is_active = true;
          question.comments = [];
          question.showDiscussion = false; // 活跃题目默认不显示讨论，需要点击按钮才展示
          question.loadingComments = false;
          question.hasAnswered = false; // 默认未回答
          
          // 检查该题目是否已经回答过（从localStorage中获取）
          const hasAnswered = answerResults.value && answerResults.value[question.id] && answerResults.value[question.id].success;
          if (hasAnswered) {
            console.log(`题目(ID: ${question.id})已回答过，标记为已回答状态`);
            // 将题目标记为已回答，但保持活跃状态以便显示在活跃题目列表中
            question.hasAnswered = true;
            
            // 确保选择的答案与结果匹配
            if (answerResults.value[question.id].correctAnswer !== undefined && 
                selectedAnswers.value[question.id] === undefined) {
              console.log(`恢复题目(ID: ${question.id})的已选答案`);
              selectedAnswers.value[question.id] = answerResults.value[question.id].correctAnswer;
              // 更新本地存储
              localStorage.setItem(`quiz_selected_answers_${presentationId.value}`, 
                                  JSON.stringify(selectedAnswers.value));
            }
          }
          
          questionsList.push(question);
        }
        console.log(`成功添加 ${activeQuestions.length} 个活跃题目`);
      } else {
        console.log(`演讲ID ${presentationId.value} 没有活跃题目`);
      }
    } catch (activeErr) {
      console.warn(`获取演讲ID ${presentationId.value} 的活跃题目失败`, activeErr);
      
      // 如果新API失败，尝试使用旧的单个活跃题目API作为备用
      try {
        const activeQuestion = await getActiveQuestion(presentationId.value);
        if (activeQuestion && !activeQuestion.msg) {
          activeQuestion.is_active = true;
          activeQuestion.comments = [];
          activeQuestion.showDiscussion = false; // 活跃题目默认不显示讨论，需要点击按钮才展示
          activeQuestion.loadingComments = false;
          activeQuestion.hasAnswered = false; // 默认未回答
          
          // 检查该题目是否已经回答过（从localStorage中获取）
          const hasAnswered = answerResults.value && 
                             answerResults.value[activeQuestion.id] && 
                             answerResults.value[activeQuestion.id].success;
          
          if (hasAnswered) {
            console.log(`单个活跃题目(ID: ${activeQuestion.id})已回答过，标记为已回答状态`);
            // 将题目标记为已回答，但保持活跃状态以便显示
            activeQuestion.hasAnswered = true;
            
            // 确保选择的答案与结果匹配
            if (answerResults.value[activeQuestion.id].correctAnswer !== undefined && 
                selectedAnswers.value[activeQuestion.id] === undefined) {
              console.log(`恢复题目(ID: ${activeQuestion.id})的已选答案`);
              selectedAnswers.value[activeQuestion.id] = answerResults.value[activeQuestion.id].correctAnswer;
              // 更新本地存储
              localStorage.setItem(`quiz_selected_answers_${presentationId.value}`, 
                                 JSON.stringify(selectedAnswers.value));
            }
          }
          
          questionsList.push(activeQuestion);
        }
      } catch (fallbackErr) {
        console.warn(`备用方法获取演讲活跃题目也失败`, fallbackErr);
      }
    }
    
    // 获取演讲的所有问题（包括活跃和非活跃的）
    try {
      console.log(`正在获取演讲ID ${presentationId.value} 的所有问题`);
      // 使用 getPresentationQuestions 函数获取所有问题
      const response = await getPresentationQuestions(presentationId.value);
      console.log('获取到的所有问题:', response);
      
      // 从返回的数据中提取questions数组
      const allQuestions = response.questions || [];
      console.log('处理后的questions数组:', allQuestions);
      
      if (Array.isArray(allQuestions) && allQuestions.length > 0) {
        // 创建一个映射来跟踪已经添加的问题ID，避免重复
        const addedQuestionIds = new Set(questionsList.map(q => q.id));
        
        // 处理所有问题
        for (const question of allQuestions) {
          // 如果问题已经在列表中（可能是活跃问题），跳过
          if (addedQuestionIds.has(question.id)) {
            console.log(`问题ID ${question.id} 已在列表中，跳过`);
            continue;
          }
          
          console.log(`处理问题: ${question.id}, 活跃状态: ${question.is_active}`);
          
          // 确保所有必要的属性都被设置
          question.is_active = question.is_active === undefined ? false : Boolean(question.is_active);
          question.comments = [];
          question.showDiscussion = false; // 默认不显示讨论区，用户点击后才显示
          question.loadingComments = false;
          question.hasAnswered = false; // 默认未回答
            
          // 检查该题目是否已经回答过（从localStorage中获取）
          const hasAnswered = answerResults.value && 
                            answerResults.value[question.id] && 
                            answerResults.value[question.id].success;
          
          if (hasAnswered) {
            console.log(`历史题目(ID: ${question.id})已回答过，标记为已回答状态`);
            question.hasAnswered = true;
            
            // 确保选择的答案与结果匹配
            if (answerResults.value[question.id].correctAnswer !== undefined && 
                selectedAnswers.value[question.id] === undefined) {
              console.log(`恢复题目(ID: ${question.id})的已选答案`);
              selectedAnswers.value[question.id] = answerResults.value[question.id].correctAnswer;
              // 更新本地存储
              localStorage.setItem(`quiz_selected_answers_${presentationId.value}`, 
                                  JSON.stringify(selectedAnswers.value));
            }
          }
          
          questionsList.push(question);
          addedQuestionIds.add(question.id);
        }
        console.log(`成功添加所有题目，总数: ${questionsList.length}`);
      }
    } catch (err) {
      console.warn(`获取演讲ID ${presentationId.value} 的所有题目失败`, err);
      // 输出更详细的错误信息以便调试
      if (err.response) {
        console.error('错误响应详情:', {
          status: err.response.status,
          headers: err.response.headers,
          data: err.response.data
        });
      }
    }
    
    questions.value = questionsList;
    
    // 如果问题列表为空，可以在这里设置一个提示信息
    if (questions.value.length === 0) {
      console.log('当前演讲暂无测验题目');
    } else {
      // 在问题加载完成后，如果有记录的问题ID，则滚动到该问题
      setTimeout(() => {
        if (currentQuestionId.value) {
          scrollToQuestion(currentQuestionId.value);
        }
      }, 300);
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
  console.log(`尝试获取题目(ID: ${question.id})的评论, 活跃状态: ${question.is_active}`);
  
  // 注意：后端API限制已修改，允许获取所有题目的评论
  // 但如果后端仍有限制，会在评论获取逻辑中处理
  
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
        const commentsList = Array.isArray(comments) ? comments : [];
        
        // 为评论数据添加前端组件需要的属性
        question.comments = commentsList.map(comment => {
          // 将服务器返回的数据格式转换为前端组件需要的格式
          const processedComment = {
            ...comment,
            id: comment.id,
            userId: comment.user_id,
            username: comment.username,
            content: comment.comment_text,
            time: comment.timestamp,
            role: comment.role || 'listener', // 设置默认角色
          };
          
          // 处理回复评论
          if (comment.replies && Array.isArray(comment.replies)) {
            processedComment.replies = comment.replies.map(reply => {
              return {
                ...reply,
                id: reply.id,
                userId: reply.user_id,
                username: reply.username,
                content: reply.comment_text,
                time: reply.timestamp,
                role: reply.role || 'listener',
              };
            });
          }
          
          return processedComment;
        });
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
const submitComment = async (questionId, commentData) => {
  // 从 commentData 对象中提取实际的评论内容
  const commentText = typeof commentData === 'object' ? commentData.content : commentData;
  const replyToId = typeof commentData === 'object' ? commentData.replyTo : null;
  
  if (!commentText || typeof commentText !== 'string' || !commentText.trim()) return;
  
  const question = questions.value.find(q => q.id === questionId);
  if (!question) return;
  
  console.log(`尝试为题目(ID: ${questionId})添加评论, 活跃状态: ${question.is_active}`);
  console.log('评论数据:', commentData, replyToId ? `回复ID: ${replyToId}` : '');
  
  // 注意：后端API限制已修改，允许为所有题目添加评论
  // 但如果后端仍有限制，会在评论提交逻辑中处理
  
  try {
    // 准备评论数据，如果有回复ID则添加父评论ID
    const commentPayload = { 
      commentText: commentText 
    };
    
    if (replyToId) {
      commentPayload.parentCommentId = replyToId;
    }
    
    // 按照API文档，发送评论
    const response = await addComment(questionId, commentPayload);
    
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

// 回复评论功能已合并到 submitComment 方法中处理

// 切换讨论区显示状态
const toggleDiscussion = async (question) => {
  // 记录当前查看的问题ID
  currentQuestionId.value = question.id;
  localStorage.setItem(`last_viewed_question_${presentationId.value}`, question.id);
  
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
  // 记录当前交互的问题ID
  currentQuestionId.value = questionId;
  localStorage.setItem(`last_viewed_question_${presentationId.value}`, questionId);
  
  selectedAnswers.value = {
    ...selectedAnswers.value,
    [questionId]: optionIndex
  };
  // 保存选择到localStorage
  localStorage.setItem(`quiz_selected_answers_${presentationId.value}`, JSON.stringify(selectedAnswers.value));
};

// 提交问题答案
const submitQuestionAnswer = async (question) => {
  if (!question || !question.is_active) return;
  
  // 保存当前问题ID，用于后续恢复位置
  currentQuestionId.value = question.id;
  
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
      // 更新答案结果状态
      answerResults.value = {
        ...answerResults.value,
        [question.id]: {
          success: true,
          correct: result.correct || false,
          message: result.correct ? '回答正确！' : '回答错误。',
          correctAnswer: result.correct_answer
        }
      };
      
      // 标记问题为已回答状态
      question.hasAnswered = true;
      
      // 保存最终选择的答案
      selectedAnswers.value = {
        ...selectedAnswers.value,
        [question.id]: selectedOption
      };
      
      // 保存到localStorage
      localStorage.setItem(`quiz_selected_answers_${presentationId.value}`, 
                         JSON.stringify(selectedAnswers.value));
      localStorage.setItem(`quiz_answer_results_${presentationId.value}`, 
                         JSON.stringify(answerResults.value));
      
      console.log(`题目(ID: ${question.id})答案已提交并保存到本地存储`);
      
      // 使用局部更新方式替代全局刷新
      setTimeout(() => {
        updateQuestionStatus(question.id);
      }, 1000);
    } else if (result && result.msg === "You have already submitted an answer for this question") {
      // 处理重复提交的情况
      console.log(`题目(ID: ${question.id})已经回答过，更新本地状态`);
      
      // 确保在本地标记为已回答
      answerResults.value = {
        ...answerResults.value,
        [question.id]: {
          success: true, // 虽然服务器拒绝了这次提交，但我们知道该题已有答案
          message: '您已经回答过这个问题',
          alreadyAnswered: true
        }
      };
      
      // 标记问题为已回答状态
      question.hasAnswered = true;
      
      // 保存到localStorage
      localStorage.setItem(`quiz_answer_results_${presentationId.value}`, 
                         JSON.stringify(answerResults.value));
      
      // 使用局部更新方式替代全局刷新
      setTimeout(() => {
        updateQuestionStatus(question.id);
      }, 1000);
    } else {
      // 其他错误情况
      answerResults.value = {
        ...answerResults.value,
        [question.id]: {
          error: true,
          message: result.msg || '提交答案失败'
        }
      };
      
      // 保存答案结果到localStorage (即使是错误)
      localStorage.setItem(`quiz_answer_results_${presentationId.value}`, JSON.stringify(answerResults.value));
    }
  } catch (err) {
    console.error('提交答案失败:', err);
    
    // 网络错误时，假设用户已回答过此题，防止重复提交
    console.log(`提交题目(ID: ${question.id})答案时发生错误，处理为"已回答"状态`);
    
    answerResults.value = {
      ...answerResults.value,
      [question.id]: {
        success: true, // 将错误处理为成功，防止用户重复提交
        message: '您已回答过此题',
        alreadyAnswered: true
      }
    };
    
    // 标记问题为已回答状态
    question.hasAnswered = true;
    
    // 保存到localStorage
    localStorage.setItem(`quiz_answer_results_${presentationId.value}`, 
                       JSON.stringify(answerResults.value));
  } finally {
    submittingAnswer.value = false;
  }
};

// 新增方法：只更新单个问题状态，而不是全部重新获取
const updateQuestionStatus = async (questionId) => {
  try {
    // 查找问题在列表中的索引
    const questionIndex = questions.value.findIndex(q => q.id === questionId);
    if (questionIndex === -1) return;
    
    // 获取这个特定问题的最新状态
    const response = await getActiveQuestion(presentationId.value, questionId);
    
    // 如果能获取到最新状态，则更新
    if (response && !response.msg) {
      const updatedQuestion = response;
      
      // 保留现有的UI状态属性
      updatedQuestion.showDiscussion = questions.value[questionIndex].showDiscussion;
      updatedQuestion.comments = questions.value[questionIndex].comments || [];
      updatedQuestion.loadingComments = false;
      
      // 确保问题标记为已回答
      updatedQuestion.hasAnswered = true;
      updatedQuestion.is_active = response.is_active !== undefined ? response.is_active : questions.value[questionIndex].is_active;
      
      // 更新问题
      questions.value.splice(questionIndex, 1, updatedQuestion);
      console.log(`题目(ID: ${questionId})状态已更新`);
      
      // 如果问题已经不再活跃，可能需要重新获取评论
      if (!updatedQuestion.is_active && updatedQuestion.showDiscussion) {
        fetchQuestionComments(updatedQuestion);
      }
    } else {
      console.log(`无法获取题目(ID: ${questionId})的最新状态，保持当前状态`);
    }
    
    // 滚动到当前问题位置
    scrollToQuestion(questionId);
  } catch (err) {
    console.error(`更新题目(ID: ${questionId})状态失败:`, err);
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
  
  // 更新localStorage
  localStorage.setItem(`quiz_selected_answers_${presentationId.value}`, JSON.stringify(selectedAnswers.value));
  localStorage.setItem(`quiz_answer_results_${presentationId.value}`, JSON.stringify(answerResults.value));
};

// 重新加载保存的答案和结果
const reloadSavedAnswersAndResults = (presentationId) => {
  if (!presentationId) {
    console.warn('无法加载已保存的答案和结果：演讲ID为空');
    return;
  }
  
  console.log(`重新加载演讲ID ${presentationId} 的已保存答案和结果`);
  
  // 加载已选择的答案
  const savedAnswers = localStorage.getItem(`quiz_selected_answers_${presentationId}`);
  if (savedAnswers) {
    try {
      const parsed = JSON.parse(savedAnswers);
      if (parsed && typeof parsed === 'object') {
        selectedAnswers.value = parsed;
        console.log('已加载保存的答案选择:', selectedAnswers.value);
      } else {
        console.warn('保存的答案选择格式不正确，使用空对象');
        selectedAnswers.value = {};
      }
    } catch (err) {
      console.error('解析保存的答案选择时出错:', err);
      selectedAnswers.value = {};
    }
  } else {
    console.log('没有找到已保存的答案选择');
    selectedAnswers.value = {};
  }
  
  // 加载答案结果
  const savedResults = localStorage.getItem(`quiz_answer_results_${presentationId}`);
  if (savedResults) {
    try {
      const parsed = JSON.parse(savedResults);
      if (parsed && typeof parsed === 'object') {
        answerResults.value = parsed;
        console.log('已加载保存的答案结果:', answerResults.value);
      } else {
        console.warn('保存的答案结果格式不正确，使用空对象');
        answerResults.value = {};
      }
    } catch (err) {
      console.error('解析保存的答案结果时出错:', err);
      answerResults.value = {};
    }
  } else {
    console.log('没有找到已保存的答案结果');
    answerResults.value = {};
  }
};

// 监听演讲ID变化
watch(presentationId, (newId, oldId) => {
  if (newId && newId !== oldId) {
    console.log(`演讲ID变更为: ${newId}`);
    // 重新加载该演讲的已保存答案和结果
    reloadSavedAnswersAndResults(newId);
    fetchPresentationQuestions();
  }
});

// 监听演讲ID变化，自动加载相应的答案和结果
watch(() => presentationId.value, (newPresentationId, oldPresentationId) => {
  if (newPresentationId && newPresentationId !== oldPresentationId) {
    console.log(`演讲ID从 ${oldPresentationId} 变为 ${newPresentationId}，重新加载数据`);
    reloadSavedAnswersAndResults(newPresentationId);
    fetchPresentationQuestions();
  }
});

// 滚动到指定问题位置的方法
const scrollToQuestion = (questionId) => {
  if (!questionId) return;
  
  // 等待DOM更新后执行滚动
  setTimeout(() => {
    try {
      const questionElement = document.querySelector(`.question-card[data-question-id="${questionId}"]`);
      if (questionElement) {
        // 滚动到问题位置，加一点偏移量以获得更好的视觉体验
        questionElement.scrollIntoView({ behavior: 'smooth', block: 'center' });
        console.log(`滚动到题目位置(ID: ${questionId})`);
      } else {
        console.warn(`找不到题目元素(ID: ${questionId})`);
      }
    } catch (err) {
      console.error('滚动到题目位置时出错:', err);
    }
  }, 100);
};

// 组件挂载后获取题目
onMounted(() => {
  if (presentationId.value) {
    reloadSavedAnswersAndResults(presentationId.value);
  }
  fetchPresentationQuestions();
  
  // 从localStorage恢复上次查看的问题ID
  const lastViewedQuestionId = localStorage.getItem(`last_viewed_question_${presentationId.value}`);
  if (lastViewedQuestionId) {
    currentQuestionId.value = parseInt(lastViewedQuestionId);
  }
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
  border-left: 4px solid #4dc189; /* 添加绿色边框，与其他页面保持一致 */
  transition: all 0.3s ease;
}

/* 当前问题高亮样式 */
.question-card.current-question {
  box-shadow: 0 0 0 2px #4dc189, 0 4px 12px rgba(77, 193, 137, 0.2);
  transform: translateY(-2px);
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
  background: #e8f5e9;
  color: #4caf50;
}

.question-status.inactive {
  background: #e8eaed;
  color: #5f6368;
}

.question-options {
  padding: 1rem 1.5rem;
  display: flex;
  flex-direction: column;
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
  background: #4dc189;
  color: white;
  font-weight: 500;
  cursor: pointer;
  transition: background 0.2s;
}

.action-button:hover {
  background: #3aa875;
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
  background: #f0f9f6;
  transform: translateY(-2px);
  box-shadow: 0 3px 6px rgba(0,0,0,0.1);
}

.answer-option-compact.selected {
  background: #4dc189;
  color: white;
  box-shadow: 0 2px 5px rgba(77, 193, 137, 0.3);
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

/* 添加新的 ABCD 样式选项 */
.answer-options {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  margin-bottom: 1.5rem;
  padding: 0 1rem;
}

.answer-option {
  display: flex;
  align-items: center;
  padding: 0.75rem 1rem;
  border-radius: 8px;
  background: #f5f5f5;
  cursor: pointer;
  transition: all 0.2s;
  position: relative;
  border: 1px solid transparent;
}

.answer-option:hover {
  background: #f0f9f6;
  border-color: #4dc189;
}

.answer-option.selected {
  background: #f0f9f6;
  border-color: #4dc189;
  box-shadow: 0 2px 4px rgba(77, 193, 137, 0.15);
}

.answer-option.selected .option-label {
  background: #4dc189;
  color: white;
}

.answer-option.correct-answer {
  background: #f0f9f6;
  border-color: #4dc189;
}

.answer-option .option-label {
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

.answer-option .option-text {
  flex: 1;
  font-size: 1rem;
}

.answer-option .correct-mark {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 1.5rem;
  height: 1.5rem;
  background: #4caf50;
  border-radius: 50%;
  color: white;
  font-size: 1rem;
  font-weight: bold;
  margin-left: 0.75rem;
}

.answer-option .correct-text {
  color: #4caf50;
  font-weight: bold;
  margin-left: 0.5rem;
  display: inline-block;
}

/* 简化版答案选项样式 */
.answer-options-simple {
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  justify-content: center;
  gap: 1rem;
}

.answer-option-simple {
  width: 4rem;
  height: 4rem;
  justify-content: center;
  padding: 0;
  border-radius: 50%;
}

.answer-option-simple .option-label {
  margin: 0;
  font-size: 1.2rem;
  width: 3rem;
  height: 3rem;
}

.answer-option-simple .correct-text {
  position: absolute;
  bottom: -1.5rem;
  left: 50%;
  transform: translateX(-50%);
}

.answer-option-simple:hover {
  transform: translateY(-2px);
  box-shadow: 0 3px 6px rgba(0,0,0,0.1);
}

.answer-option-simple.selected {
  transform: scale(1.05);
}

/* 已回答题目的样式 */
.already-answered-notice {
  text-align: center;
  padding: 0.5rem 0;
  margin-top: 1rem;
  background: #f0f9f6;
  border-radius: 4px;
  color: #4dc189;
  font-size: 0.9rem;
  font-weight: 500;
}

.question-answered .answer-option-simple {
  opacity: 0.8;
  cursor: default;
}

.question-answered .answer-option-simple:hover {
  transform: none;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}
</style>
