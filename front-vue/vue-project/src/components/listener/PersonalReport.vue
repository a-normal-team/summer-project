<template>
  <div class="sub-dashboard-section">
    <h2>个人报告</h2>
    
    <div v-if="!selectedPresentationId" class="no-selection">
      <div v-if="presentations.length === 0" class="empty-state">
        <p>您还未参与任何演讲，暂无个人报告</p>
      </div>
      <div v-else class="presentation-selection">
        <h3>选择要查看的演讲报告</h3>
        <div class="presentation-list">
          <div v-for="presentation in presentations" :key="presentation.id" class="presentation-item">
            <h3>{{ presentation.title }}</h3>
            <p>{{ presentation.description }}</p>
            <p>演讲者: {{ presentation.speaker || '未分配' }}</p>
            <div class="action-buttons">
              <button @click="selectPresentation(presentation)" class="select-button">
                查看报告
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <div v-else-if="loading" class="loading-state">
      <p>加载中...</p>
    </div>
    
    <div v-else-if="error" class="error-state">
      <p>{{ error }}</p>
      <button @click="fetchReport" class="retry-button">重试</button>
    </div>
    
    <div v-else-if="hasActiveQuestions" class="waiting-state">
      <div class="waiting-icon">
        <i class="waiting-spinner"></i>
      </div>
      <p>等待所有题目回答完毕后展示</p>
      <p class="waiting-sub-text">当前演讲中仍有进行中的题目</p>
      <button @click="fetchReport" class="retry-button">刷新状态</button>
    </div>
    
    <div v-else class="report-content">
      <div class="presentation-header">
        <h3>{{ selectedPresentation?.title }}</h3>
        <p>演讲者: {{ selectedPresentation?.speaker || '未分配' }}</p>
        <button @click="clearSelection" class="manage-button">返回演讲列表</button>
      </div>
      
      <div class="stats-section">
        <h3>个人表现统计</h3>
        <div class="stats-grid">
          <div class="stat-item">
            <div class="stat-label">演讲总题目数</div>
            <div class="stat-value">{{ report.total_questions_in_presentation || 0 }}</div>
          </div>
          <div class="stat-item">
            <div class="stat-label">已回答题目</div>
            <div class="stat-value">{{ report.answered_questions || 0 }}</div>
          </div>
          <div class="stat-item">
            <div class="stat-label">回答正确数</div>
            <div class="stat-value">{{ report.correct_answers || 0 }}</div>
          </div>
          <div class="stat-item">
            <div class="stat-label">正确率</div>
            <div class="stat-value">{{ report.accuracy_rate || '0%' }}</div>
          </div>
        </div>
      </div>
      
      <div v-if="report.question_details && report.question_details.length > 0" class="questions-section">
        <h3>题目详情</h3>
        <div class="question-list">
          <div v-for="(question, index) in report.question_details" :key="question.question_id" class="question-item">
            <div class="question-header">
              <div class="question-number">题目 #{{ index + 1 }}</div>
              <div :class="['question-status', question.is_correct ? 'correct' : 'incorrect']">
                {{ question.is_correct ? '✓ 正确' : '✗ 错误' }}
              </div>
            </div>
            <div class="question-text">{{ question.question_text }}</div>
            <div class="question-details">
              <div class="detail-row">
                <div class="detail-label">您的答案:</div>
                <div class="detail-value">{{ question.your_answer }}</div>
              </div>
              <div v-if="!question.is_correct" class="detail-row">
                <div class="detail-label">正确答案:</div>
                <div class="detail-value correct">{{ question.correct_answer }}</div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div v-else class="empty-questions">
        <p>暂无题目详情</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import { getPresentations } from '../../services/presentation';
import { getUserReport, getActiveQuestions } from '../../services/quiz';
import { authState, getUserId } from '../../services/auth';

// 状态变量
const presentations = ref([]);
const selectedPresentationId = ref(null);
const selectedPresentation = ref(null);
const report = ref({});
const loading = ref(false);
const error = ref(null);
const hasActiveQuestions = ref(false); // 跟踪是否存在活跃题目

// 页面加载时获取已参与的演讲
onMounted(async () => {
  await fetchParticipatedPresentations();
  
  // 从localStorage获取已选择的演讲信息
  const storedPresentation = localStorage.getItem('selectedPresentation');
  if (storedPresentation) {
    try {
      const parsedPresentation = JSON.parse(storedPresentation);
      selectedPresentationId.value = parsedPresentation.id;
      const found = presentations.value.find(p => p.id === parsedPresentation.id);
      if (found) {
        selectedPresentation.value = found;
        fetchReport();
      }
    } catch (err) {
      console.error('Error parsing selected presentation:', err);
    }
  }
});

// 监听选中的演讲ID变化
watch(selectedPresentationId, (newValue) => {
  if (newValue) {
    const found = presentations.value.find(p => p.id === newValue);
    if (found) {
      selectedPresentation.value = found;
      fetchReport();
    }
  } else {
    selectedPresentation.value = null;
    report.value = {};
  }
});

// 获取参与过的演讲
const fetchParticipatedPresentations = async () => {
  if (!authState.isAuthenticated) {
    error.value = '请先登录';
    return;
  }
  
  loading.value = true;
  error.value = null;
  
  try {
    // 以listener角色获取参与过的演讲
    const data = await getPresentations('listener');
    
    if (Array.isArray(data)) {
      presentations.value = data;
    } else {
      presentations.value = [];
      error.value = '数据格式错误，请联系管理员';
    }
  } catch (err) {
    console.error('获取参与的演讲列表失败:', err);
    error.value = err.message || '获取演讲列表失败，请稍后再试';
    presentations.value = [];
  } finally {
    loading.value = false;
  }
};

// 获取个人报告
const fetchReport = async () => {
  if (!selectedPresentationId.value) return;
  
  loading.value = true;
  error.value = null;
  
  try {
    // 首先检查演讲是否有活跃的题目
    try {
      const activeQuestions = await getActiveQuestions(selectedPresentationId.value);
      hasActiveQuestions.value = Array.isArray(activeQuestions) && activeQuestions.length > 0;
      if (hasActiveQuestions.value) {
        console.log('当前演讲有活跃题目，等待所有题目回答完毕后才能显示报告');
        loading.value = false;
        return; // 如果有活跃题目，提前返回，不加载报告内容
      }
    } catch (activeErr) {
      console.warn('检查活跃题目失败:', activeErr);
      // 继续执行，即使检查活跃题目失败
    }
    
    // 使用getUserId辅助函数获取当前用户ID
    const currentUserId = getUserId();
    if (!currentUserId) {
      throw new Error('无法获取当前用户ID');
    }
    
    // 调用API获取个人报告
    const data = await getUserReport(selectedPresentationId.value, currentUserId);
    report.value = data;
    hasActiveQuestions.value = false; // 确保设置为false
  } catch (err) {
    console.error('获取个人报告失败:', err);
    error.value = err.message || '获取个人报告失败，请稍后再试';
    
    // 如果API调用失败，使用模拟数据作为后备方案
    report.value = {
      listener_id: currentUserId || 0,
      listener_username: authState.user?.username || localStorage.getItem('username') || "当前用户",
      presentation_id: selectedPresentationId.value,
      presentation_title: selectedPresentation.value?.title || "未知演讲",
      total_questions_in_presentation: 5,
      answered_questions: 5,
      correct_answers: 3,
      accuracy_rate: "60.00%",
      question_details: [
        {
          question_id: 1,
          question_text: "Flask 是一个什么类型的框架？",
          your_answer: "微框架",
          is_correct: true,
          correct_answer: "微框架"
        },
        {
          question_id: 2,
          question_text: "Python 的创始人是谁？",
          your_answer: "James Gosling",
          is_correct: false,
          correct_answer: "Guido van Rossum"
        },
        {
          question_id: 3,
          question_text: "HTML5 发布于哪一年？",
          your_answer: "2014",
          is_correct: true,
          correct_answer: "2014"
        },
        {
          question_id: 4,
          question_text: "React 由哪家公司开发？",
          your_answer: "Facebook",
          is_correct: true,
          correct_answer: "Facebook"
        },
        {
          question_id: 5,
          question_text: "哪种方法用于处理 JavaScript 中的异步操作？",
          your_answer: "回调函数",
          is_correct: false,
          correct_answer: "Promises"
        }
      ]
    };
  } finally {
    loading.value = false;
  }
};

// 选择演讲
const selectPresentation = (presentation) => {
  selectedPresentationId.value = presentation.id;
  localStorage.setItem('selectedPresentation', JSON.stringify({
    id: presentation.id,
    title: presentation.title
  }));
};

// 清除选择
const clearSelection = () => {
  selectedPresentationId.value = null;
  localStorage.removeItem('selectedPresentation');
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
  box-sizing: border-box; /* 确保padding不会增加容器实际尺寸 */
  min-height: 0; /* 确保flex项可以正确计算overflow */
}

h2 {
  color: #4dc189;
  margin-bottom: 20px;
}

h3 {
  color: #333;
  margin: 15px 0 10px 0;
}

.no-selection, .loading-state, .error-state, .empty-state, .waiting-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 30px 20px;
  text-align: center;
}

.error-state {
  color: #e74c3c;
}

.waiting-state {
  color: #4dc189;
}

.waiting-icon {
  margin-bottom: 20px;
  position: relative;
  width: 50px;
  height: 50px;
}

.waiting-spinner {
  display: inline-block;
  width: 100%;
  height: 100%;
  border: 4px solid rgba(77, 193, 137, 0.3);
  border-radius: 50%;
  border-top-color: #4dc189;
  animation: spin 1s ease-in-out infinite;
}

.waiting-sub-text {
  font-size: 14px;
  opacity: 0.8;
  margin-top: 5px;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.retry-button, .select-button {
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
  margin-top: 15px;
}

.retry-button:hover, .select-button:hover {
  background-color: #3aa875;
  transform: translateY(-1px);
}

.presentation-header {
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 1px solid #eee;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.manage-button {
  border-radius: 20px;
  border: 1px solid #3aa875;
  background-color: #ffffff;
  color: #3aa875;
  font-size: 11px;
  font-weight: bold;
  padding: 6px 10px;
  letter-spacing: 1px;
  text-transform: uppercase;
  transition: all 0.3s ease;
  cursor: pointer;
  margin-top: 10px;
}

.manage-button:hover {
  background-color: #f0f9f6;
  transform: translateY(-1px);
}

.presentation-selection {
  width: 100%;
}

.presentation-list {
  display: grid;
  gap: 20px;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  padding-bottom: 30px;
  margin-bottom: 20px;
}

.presentation-item {
  background-color: #f9f9f9;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.presentation-item h3 {
  color: #333;
  margin-bottom: 10px;
}

.presentation-item p {
  color: #666;
  margin-bottom: 8px;
  font-size: 14px;
}

.action-buttons {
  display: flex;
  justify-content: flex-end;
  margin-top: 10px;
}

.stats-section {
  margin-bottom: 30px;
  padding: 15px;
  background-color: #f9f9f9;
  border-radius: 8px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: 15px;
  margin-top: 15px;
}

.stat-item {
  background-color: #fff;
  padding: 15px;
  border-radius: 8px;
  text-align: center;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.stat-label {
  font-size: 12px;
  color: #666;
  margin-bottom: 5px;
}

.stat-value {
  font-size: 24px;
  font-weight: 600;
  color: #4dc189;
}

.questions-section {
  margin-bottom: 30px;
}

.question-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
  margin-top: 15px;
}

.question-item {
  background-color: #f9f9f9;
  padding: 15px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.question-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 10px;
}

.question-number {
  font-weight: 600;
  color: #333;
}

.question-status {
  font-weight: 600;
  padding: 2px 8px;
  border-radius: 4px;
}

.question-status.correct {
  color: #4dc189;
}

.question-status.incorrect {
  color: #e74c3c;
}

.question-text {
  font-size: 16px;
  margin-bottom: 15px;
  padding: 10px;
  background-color: #fff;
  border-radius: 6px;
}

.question-details {
  background-color: #fff;
  padding: 10px;
  border-radius: 6px;
}

.detail-row {
  display: flex;
  margin-bottom: 5px;
}

.detail-label {
  font-weight: 600;
  width: 100px;
  color: #666;
}

.detail-value {
  flex-grow: 1;
}

.detail-value.correct {
  color: #4dc189;
}

.empty-questions {
  text-align: center;
  padding: 30px;
  color: #666;
}
</style>
