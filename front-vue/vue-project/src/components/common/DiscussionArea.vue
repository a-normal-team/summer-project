<template>
  <div class="discussion-area">
    <div class="discussion-header">
      <h3>讨论区</h3>
      <span class="comment-count">{{ comments.length }}条评论</span>
    </div>
    
    <div class="comments-list" ref="commentsList">
      <div v-for="comment in comments" :key="comment.id" class="comment-item">
        <div class="comment-header">
          <div class="user-info">
            <span class="username">{{ comment.username }}</span>
            <span class="role-tag" :class="comment.role">{{ getRoleText(comment.role) }}</span>
          </div>
          <span class="comment-time">{{ formatTime(comment.time || comment.timestamp) }}</span>
        </div>
        <div class="comment-content">{{ comment.content || comment.comment_text }}</div>
        <div class="comment-actions">
          <button 
            class="action-link" 
            :class="{'replying': replyingTo === comment.id}"
            @click="toggleReplyTo(comment)"
          >
            {{ replyingTo === comment.id ? '正在回复...' : '回复' }}
          </button>
        </div>
        
        <!-- 回复列表 -->
        <div v-if="comment.replies && comment.replies.length > 0" class="replies-list">
          <div v-for="reply in comment.replies" :key="reply.id" class="reply-item">
            <div class="comment-header">
              <div class="user-info">
                <span class="username">{{ reply.username }}</span>
                <span class="role-tag" :class="reply.role">{{ getRoleText(reply.role) }}</span>
              </div>
              <span class="comment-time">{{ formatTime(reply.time || reply.timestamp) }}</span>
            </div>
            <div class="comment-content">{{ reply.content || reply.comment_text }}</div>
          </div>
        </div>
      </div>
    </div>

    <!-- 评论输入框 -->
    <div class="comment-input-area">
      <textarea
        v-model="newComment"
        placeholder="发表评论..."
        :disabled="!isLoggedIn"
        @keydown.enter.prevent="submitComment"
      ></textarea>
      <button 
        class="action-button"
        @click="submitComment"
        :disabled="!canSubmit"
      >
        发送
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, defineProps, defineEmits } from 'vue';

const props = defineProps({
  comments: {
    type: Array,
    required: true
  },
  currentUser: {
    type: Object,
    required: true
  },
  isLoggedIn: {
    type: Boolean,
    default: false
  }
});

const emit = defineEmits(['submit', 'reply', 'delete']);

const newComment = ref('');
const replyingTo = ref(null);

const canSubmit = computed(() => {
  return props.isLoggedIn && newComment.value.trim().length > 0;
});

const getRoleText = (role) => {
  const roleMap = {
    'speaker': '演讲者',
    'listener': '听众',
    'organizer': '组织者'
  };
  return roleMap[role] || role;
};

const formatTime = (time) => {
  if (!time) return '刚刚'; // 如果时间为空，显示"刚刚"
  
  try {
    const date = new Date(time);
    // 检查日期是否有效
    if (isNaN(date.getTime())) {
      return '刚刚';
    }
    
    return date.toLocaleString('zh-CN', {
      month: 'numeric',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  } catch (err) {
    console.error('格式化时间出错:', err);
    return '刚刚';
  }
};

const submitComment = () => {
  if (canSubmit.value) {
    emit('submit', {
      content: newComment.value,
      replyTo: replyingTo.value
    });
    newComment.value = '';
    replyingTo.value = null;
  }
};

const toggleReplyTo = (comment) => {
  // 如果当前已经在回复这条评论，则取消回复状态
  if (replyingTo.value === comment.id) {
    replyingTo.value = null;
  } else {
    // 否则设置为正在回复该评论
    replyingTo.value = comment.id;
    emit('reply', comment);
  }
};

// 保留canDelete函数以防其他地方引用，但删除实际的删除功能
const canDelete = (comment) => {
  return false; // 直接返回false禁用所有删除按钮
};
</script>

<style scoped>
.discussion-area {
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.discussion-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #eee;
  padding-bottom: 10px;
}

.discussion-header h3 {
  color: #4dc189;
  margin: 0;
}

.comment-count {
  color: #666;
  font-size: 14px;
}

.comments-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
  max-height: 500px;
  overflow-y: auto;
}

.comment-item {
  background-color: #f9f9f9;
  border-radius: 6px;
  padding: 15px;
}

.comment-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 8px;
}

.username {
  font-weight: bold;
  color: #333;
}

.role-tag {
  padding: 2px 8px;
  border-radius: 10px;
  font-size: 12px;
  color: white;
}

.role-tag.speaker {
  background-color: #4dc189;
}

.role-tag.listener {
  background-color: #17a2b8;
}

.role-tag.organizer {
  background-color: #ffc107;
  color: #333;
}

.comment-time {
  color: #999;
  font-size: 12px;
}

.comment-content {
  color: #333;
  line-height: 1.5;
  margin-bottom: 10px;
}

.comment-actions {
  display: flex;
  gap: 15px;
}

.action-link {
  background: none;
  border: none;
  color: #4dc189;
  font-size: 12px;
  cursor: pointer;
  padding: 0;
}

.action-link:hover {
  text-decoration: underline;
}

.action-link.replying {
  background-color: rgba(77, 193, 137, 0.1);
  color: #3aa875;
  font-weight: bold;
  padding: 2px 8px;
  border-radius: 12px;
}

.action-link.delete {
  color: #dc3545;
}

.replies-list {
  margin-top: 10px;
  margin-left: 20px;
  border-left: 2px solid #eee;
  padding-left: 15px;
}

.reply-item {
  background-color: #fff;
  border-radius: 6px;
  padding: 10px;
  margin-bottom: 8px;
}

.comment-input-area {
  display: flex;
  gap: 10px;
  align-items: flex-start;
}

textarea {
  flex-grow: 1;
  min-height: 60px;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 6px;
  resize: vertical;
  font-size: 14px;
}

textarea:focus {
  outline: none;
  border-color: #4dc189;
  box-shadow: 0 0 0 2px rgba(77, 193, 137, 0.1);
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

.action-button:hover:not(:disabled) {
  background-color: #3aa875;
  transform: translateY(-1px);
}

.action-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* 滚动条样式 */
.comments-list::-webkit-scrollbar {
  width: 6px;
}

.comments-list::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

.comments-list::-webkit-scrollbar-thumb {
  background: #4dc189;
  border-radius: 3px;
}

.comments-list::-webkit-scrollbar-thumb:hover {
  background: #3aa875;
}
</style>
