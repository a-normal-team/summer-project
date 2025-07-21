<template>
  <div class="feedback-ticker">
    <div class="feedback-header">
      <h3>实时反馈</h3>
      <span class="feedback-count" v-if="showCount">{{ feedbacks.length }}条反馈</span>
    </div>
    <div class="feedback-list" ref="feedbackList">
      <div 
        v-for="(feedback, index) in feedbacks" 
        :key="index"
        class="feedback-item"
        :class="feedback.type"
      >
        <div class="feedback-content">
          <span class="feedback-text">{{ feedback.text }}</span>
          <span class="feedback-time">{{ formatTime(feedback.time) }}</span>
        </div>
        <div class="feedback-count" v-if="feedback.count > 1">
          x{{ feedback.count }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineProps, ref, onMounted, watch } from 'vue';

const props = defineProps({
  feedbacks: {
    type: Array,
    required: true
  },
  showCount: {
    type: Boolean,
    default: true
  }
});

const feedbackList = ref(null);

const formatTime = (time) => {
  return new Date(time).toLocaleTimeString('zh-CN', { 
    hour: '2-digit', 
    minute: '2-digit' 
  });
};

watch(() => props.feedbacks, () => {
  if (feedbackList.value) {
    // 自动滚动到最新的反馈
    setTimeout(() => {
      feedbackList.value.scrollTop = feedbackList.value.scrollHeight;
    }, 100);
  }
}, { deep: true });

onMounted(() => {
  if (feedbackList.value) {
    feedbackList.value.scrollTop = feedbackList.value.scrollHeight;
  }
});
</script>

<style scoped>
.feedback-ticker {
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  padding: 15px;
  max-height: 400px;
  display: flex;
  flex-direction: column;
}

.feedback-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
  padding-bottom: 10px;
  border-bottom: 1px solid #eee;
}

.feedback-header h3 {
  color: #4dc189;
  margin: 0;
}

.feedback-header .feedback-count {
  color: #666;
  font-size: 14px;
}

.feedback-list {
  overflow-y: auto;
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.feedback-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px;
  background-color: #f9f9f9;
  border-radius: 6px;
  transition: all 0.3s ease;
}

.feedback-item:hover {
  transform: translateY(-1px);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.feedback-content {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.feedback-text {
  color: #333;
  font-size: 14px;
}

.feedback-time {
  color: #999;
  font-size: 12px;
}

.feedback-count {
  background-color: #4dc189;
  color: white;
  padding: 2px 6px;
  border-radius: 10px;
  font-size: 12px;
  min-width: 24px;
  text-align: center;
}

/* 反馈类型样式 */
.feedback-item.speed {
  border-left: 3px solid #ffc107;
}

.feedback-item.content {
  border-left: 3px solid #17a2b8;
}

.feedback-item.question {
  border-left: 3px solid #dc3545;
}

/* 滚动条样式 */
.feedback-list::-webkit-scrollbar {
  width: 6px;
}

.feedback-list::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

.feedback-list::-webkit-scrollbar-thumb {
  background: #4dc189;
  border-radius: 3px;
}

.feedback-list::-webkit-scrollbar-thumb:hover {
  background: #3aa875;
}
</style>
