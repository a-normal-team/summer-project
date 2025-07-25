<template>
  <div class="sub-dashboard-section">
    <h2>当前演讲</h2>
    
    <div v-if="!selectedPresentationId" class="no-selection">
      <p>请先在"可参与演讲"中选择一个演讲参与</p>
    </div>
    
    <div v-else-if="loading" class="loading-state">
      <p>加载中...</p>
    </div>
    
    <div v-else-if="error" class="error-state">
      <p>{{ error }}</p>
      <button @click="fetchPresentationDetails" class="retry-button">重试</button>
    </div>
    
    <div v-else>
      <!-- 演讲信息 -->
      <div class="presentation-header">
        <h3>{{ presentationDetails?.title }}</h3>
        <p>{{ presentationDetails?.description }}</p>
        <p>演讲者: {{ presentationDetails?.speaker || '未分配' }}</p>
        <p>状态: {{ getStatusText(presentationDetails?.status) }}</p>
      </div>
      
      <!-- 即时反馈面板 -->
      <div class="content-section">
        <FeedbackPanel @feedback="handleFeedback" />
      </div>
      
      <!-- 提示前往题目页面 -->
      <div class="content-section">
        <h3>题目与评论</h3>
        <div class="navigation-prompt">
          <p>请前往"<router-link to="/listener/dashboard/current-questions">当前题目</router-link>"页面查看和参与演讲中的题目讨论</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, onBeforeUnmount } from 'vue';
import { getPresentationById } from '../../services/presentation';
import { initWebSocket, closeWebSocket, sendFeedback } from '../../services/websocket';
import FeedbackPanel from './FeedbackPanel.vue';

// 状态变量
const selectedPresentationId = ref(null);
const presentationDetails = ref(null);
const loading = ref(false);
const error = ref(null);

// 反馈处理已移至FeedbackPanel组件中

// 页面加载时获取已选择的演讲信息并初始化Socket.IO连接
onMounted(() => {
  const storedPresentation = localStorage.getItem('selectedPresentation');
  if (storedPresentation) {
    try {
      const parsedPresentation = JSON.parse(storedPresentation);
      selectedPresentationId.value = parsedPresentation.id;
      fetchPresentationDetails();
      
      // 初始化Socket.IO连接
      initWebSocket(parsedPresentation.id, 'listener');
      
      // 注册反馈结果处理函数
      registerMessageHandler('feedback_result', (data) => {
        console.log('收到反馈结果:', data);
        
        // 显示服务器返回的结果
        const feedbackResultMessage = document.createElement('div');
        feedbackResultMessage.textContent = data.message || '反馈已处理';
        feedbackResultMessage.className = `feedback-toast ${data.success ? 'success' : 'error'}`;
        document.body.appendChild(feedbackResultMessage);
        
        // 2秒后自动移除提示
        setTimeout(() => {
          feedbackResultMessage.classList.add('fade-out');
          setTimeout(() => {
            if (document.body.contains(feedbackResultMessage)) {
              document.body.removeChild(feedbackResultMessage);
            }
          }, 300);
        }, 2000);
      });
      
    } catch (err) {
      console.error('Error parsing selected presentation:', err);
    }
  }
});

// 组件卸载前关闭WebSocket连接
onBeforeUnmount(() => {
  closeWebSocket();
});

// 监听选中的演讲ID变化
watch(selectedPresentationId, (newValue) => {
  if (newValue) {
    fetchPresentationDetails();
  } else {
    presentationDetails.value = null;
  }
});

// 获取演讲详情
const fetchPresentationDetails = async () => {
  if (!selectedPresentationId.value) return;
  
  try {
    loading.value = true;
    error.value = null;
    
    // 以listener角色获取演讲详情
    const data = await getPresentationById(selectedPresentationId.value, 'listener');
    presentationDetails.value = data;
  } catch (err) {
    console.error('获取演讲详情失败:', err);
    error.value = '获取演讲详情失败: ' + (err.message || '未知错误');
  } finally {
    loading.value = false;
  }
};

// 获取活跃题目（模拟）
const fetchActiveQuestion = async () => {
  // 这里应该调用API获取活跃题目
  // 暂时使用模拟数据
  activeQuestion.value = {
    id: 1,
    question_text: "Flask 是一个什么类型的框架？",
    question_type: "multiple_choice",
    options: ["微框架", "全栈框架", "前端框架", "数据库框架"]
  };
};

// 获取评论（模拟）
const fetchComments = async () => {
  // 这里应该调用API获取评论
  // 暂时使用模拟数据
  comments.value = [
    {
      id: 1,
      user_id: 2,
      username: "listener_one",
      comment_text: "我觉得这个题目很有趣！",
      timestamp: "2025-07-19T16:45:00.123456",
      replies: [
        {
          id: 2,
          user_id: 3,
          username: "listener_two",
          comment_text: "同意，我也觉得很有趣。",
          timestamp: "2025-07-19T16:46:00.789012",
          replies: []
        }
      ]
    }
  ];
};

// 选择选项
const selectOption = (option) => {
  selectedOption.value = option;
};

// 提交答案
const submitAnswer = async () => {
  if (!selectedOption.value) return;
  
  submitting.value = true;
  
  try {
    // 这里应该调用API提交答案
    console.log(`提交答案: ${selectedOption.value}`);
    
    // 模拟提交成功
    setTimeout(() => {
      alert(`您的答案已提交：${selectedOption.value}`);
      selectedOption.value = null;
      submitting.value = false;
    }, 1000);
  } catch (err) {
    console.error('提交答案失败:', err);
    alert('提交答案失败: ' + (err.message || '未知错误'));
    submitting.value = false;
  }
};

// 处理从FeedbackPanel接收的反馈
const handleFeedback = async (feedback) => {
  try {
    // 通过Socket.IO发送反馈
    const success = sendFeedback(selectedPresentationId.value, feedback.type);
    
    if (success) {
      console.log(`已通过Socket.IO发送反馈:`, feedback);
      // 显示成功提示，但使用更友好的非阻塞方式
      const feedbackMessage = document.createElement('div');
      feedbackMessage.textContent = '反馈已发送';
      feedbackMessage.className = 'feedback-toast success';
      document.body.appendChild(feedbackMessage);
      
      // 2秒后自动移除提示
      setTimeout(() => {
        feedbackMessage.classList.add('fade-out');
        setTimeout(() => {
          if (document.body.contains(feedbackMessage)) {
            document.body.removeChild(feedbackMessage);
          }
        }, 300);
      }, 2000);
    } else {
      throw new Error('发送反馈失败，请稍后再试');
    }
  } catch (err) {
    console.error('提交反馈失败:', err);
    
    // 显示错误提示，使用非阻塞方式
    const errorMessage = document.createElement('div');
    errorMessage.textContent = '提交反馈失败: ' + (err.message || '未知错误');
    errorMessage.className = 'feedback-toast error';
    document.body.appendChild(errorMessage);
    
    // 3秒后自动移除提示
    setTimeout(() => {
      errorMessage.classList.add('fade-out');
      setTimeout(() => {
        if (document.body.contains(errorMessage)) {
          document.body.removeChild(errorMessage);
        }
      }, 300);
    }, 3000);
  }
};

// 添加评论
const addComment = async () => {
  if (!newComment.trim()) return;
  
  try {
    // 这里应该调用API添加评论
    console.log(`添加评论: ${newComment}`);
    
    // 模拟添加成功
    const newCommentObj = {
      id: Date.now(),
      user_id: 99,
      username: "当前用户",
      comment_text: newComment,
      timestamp: new Date().toISOString(),
      replies: []
    };
    
    comments.value.push(newCommentObj);
    newComment.value = '';
    
    alert('评论已添加');
  } catch (err) {
    console.error('添加评论失败:', err);
    alert('添加评论失败: ' + (err.message || '未知错误'));
  }
};

// 回复评论
const replyToComment = async (commentId) => {
  const replyContent = replyText.value[commentId];
  if (!replyContent || !replyContent.trim()) return;
  
  try {
    // 这里应该调用API回复评论
    console.log(`回复评论${commentId}: ${replyContent}`);
    
    // 模拟回复成功
    const comment = comments.value.find(c => c.id === commentId);
    if (comment) {
      const newReply = {
        id: Date.now(),
        user_id: 99,
        username: "当前用户",
        comment_text: replyContent,
        timestamp: new Date().toISOString(),
        replies: []
      };
      
      if (!comment.replies) {
        comment.replies = [];
      }
      
      comment.replies.push(newReply);
      replyText.value[commentId] = '';
      
      alert('回复已添加');
    }
  } catch (err) {
    console.error('回复评论失败:', err);
    alert('回复评论失败: ' + (err.message || '未知错误'));
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

.no-selection, .loading-state, .error-state, .empty-section {
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

.retry-button {
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

.retry-button:hover {
  background-color: #3aa875;
  transform: translateY(-1px);
}

.presentation-header {
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 1px solid #eee;
}

.content-section {
  margin-bottom: 30px;
  padding: 15px;
  background-color: #f9f9f9;
  border-radius: 8px;
}

.active-question {
  padding: 15px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background-color: #fff;
}

.question-text {
  font-size: 16px;
  font-weight: 500;
  margin-bottom: 15px;
}

.options {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 10px;
  margin-bottom: 15px;
}

.option-button {
  border-radius: 20px;
  border: 1px solid #6c757d;
  background-color: #fff;
  color: #6c757d;
  font-size: 12px;
  padding: 8px 16px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
}

.option-button:hover {
  background-color: #f0f9f6;
}

.option-button.selected {
  border-color: #4dc189;
  background-color: #4dc189;
  color: #fff;
}

.select-button {
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
  display: block;
  margin-left: auto;
}

.select-button:hover:not(:disabled) {
  background-color: #3aa875;
  transform: translateY(-1px);
}

.select-button:disabled {
  background-color: #cccccc;
  border-color: #cccccc;
  cursor: not-allowed;
}

.feedback-section {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  padding: 10px;
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
}

.manage-button:hover {
  background-color: #f0f9f6;
  transform: translateY(-1px);
}

.manage-button.small {
  font-size: 10px;
  padding: 4px 8px;
}

.comments-section {
  margin-top: 15px;
}

.comment-item {
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 8px;
  margin-bottom: 15px;
  background-color: #fff;
}

.comment-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 5px;
  font-size: 12px;
}

.username {
  font-weight: bold;
  color: #4dc189;
}

.timestamp {
  color: #999;
}

.comment-text {
  font-size: 14px;
  margin-bottom: 10px;
}

.replies-section {
  margin-left: 20px;
  margin-top: 10px;
  padding-left: 10px;
  border-left: 2px solid #eee;
}

.reply-item {
  margin-bottom: 10px;
}

.reply-form, .comment-form {
  display: flex;
  gap: 10px;
  margin-top: 10px;
}

.reply-input, .comment-input {
  flex-grow: 1;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
}

.comment-input {
  width: 100%;
  min-height: 60px;
  margin-bottom: 10px;
  resize: vertical;
}

/* 反馈提示样式 */
.feedback-toast {
  position: fixed;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  padding: 10px 20px;
  border-radius: 4px;
  font-weight: 500;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
  z-index: 1000;
  transition: opacity 0.3s, transform 0.3s;
}

.feedback-toast.success {
  background-color: #4dc189;
  color: white;
}

.feedback-toast.error {
  background-color: #e74c3c;
  color: white;
}

.feedback-toast.fade-out {
  opacity: 0;
  transform: translateX(-50%) translateY(10px);
}
</style>
