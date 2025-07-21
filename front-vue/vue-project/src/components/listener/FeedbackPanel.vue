<template>
  <div class="feedback-panel">
    <h3>即时反馈</h3>
    <div class="feedback-buttons">
      <button 
        v-for="feedback in feedbackOptions" 
        :key="feedback.type"
        class="feedback-button"
        :class="[feedback.type, { 'active': activeFeedbacks.includes(feedback.type) }]"
        @click="submitFeedback(feedback)"
        :disabled="feedbackDisabled"
      >
        <span class="feedback-icon">{{ feedback.icon }}</span>
        {{ feedback.text }}
        <span v-if="feedbackCounts[feedback.type]" class="feedback-count">
          {{ feedbackCounts[feedback.type] }}
        </span>
      </button>
    </div>
    <div v-if="showCooldown" class="cooldown-notice">
      请等待 {{ cooldownTime }} 秒后再次提交反馈
    </div>
  </div>
</template>

<script setup>
import { ref, defineEmits } from 'vue';

const emit = defineEmits(['feedback']);

const feedbackOptions = [
  { type: 'too-fast', text: '讲得太快', icon: '⚡' },
  { type: 'too-slow', text: '讲得太慢', icon: '🐌' },
  { type: 'boring', text: '内容乏味', icon: '😴' },
  { type: 'poor-quality', text: '题目质量差', icon: '👎' },
  { type: 'confusing', text: '内容难懂', icon: '🤔' },
  { type: 'interesting', text: '内容有趣', icon: '👍' }
];

const activeFeedbacks = ref([]);
const feedbackCounts = ref({});
const feedbackDisabled = ref(false);
const cooldownTime = ref(0);
const showCooldown = ref(false);

const COOLDOWN_DURATION = 30; // 冷却时间（秒）

const startCooldown = () => {
  feedbackDisabled.value = true;
  showCooldown.value = true;
  cooldownTime.value = COOLDOWN_DURATION;

  const timer = setInterval(() => {
    cooldownTime.value--;
    if (cooldownTime.value <= 0) {
      clearInterval(timer);
      feedbackDisabled.value = false;
      showCooldown.value = false;
    }
  }, 1000);
};

const submitFeedback = (feedback) => {
  if (feedbackDisabled.value) return;

  const isActive = activeFeedbacks.value.includes(feedback.type);
  
  if (!isActive) {
    activeFeedbacks.value.push(feedback.type);
    feedbackCounts.value[feedback.type] = (feedbackCounts.value[feedback.type] || 0) + 1;
    
    emit('feedback', {
      type: feedback.type,
      text: feedback.text,
      timestamp: new Date()
    });

    startCooldown();
  }
};
</script>

<style scoped>
.feedback-panel {
  background-color: #fff;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

h3 {
  color: #4dc189;
  margin-bottom: 15px;
}

.feedback-buttons {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 10px;
}

.feedback-button {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 10px 15px;
  border: 1px solid #ddd;
  border-radius: 20px;
  background-color: #fff;
  color: #333;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
}

.feedback-icon {
  margin-right: 8px;
  font-size: 16px;
}

.feedback-button:hover:not(:disabled) {
  border-color: #4dc189;
  background-color: #f0f9f4;
}

.feedback-button.active {
  background-color: #4dc189;
  border-color: #4dc189;
  color: #fff;
}

.feedback-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* 不同类型的反馈按钮样式 */
.feedback-button.too-fast:hover:not(:disabled) {
  border-color: #ffc107;
  background-color: #fff3cd;
}

.feedback-button.too-slow:hover:not(:disabled) {
  border-color: #17a2b8;
  background-color: #d1ecf1;
}

.feedback-button.boring:hover:not(:disabled),
.feedback-button.poor-quality:hover:not(:disabled) {
  border-color: #dc3545;
  background-color: #f8d7da;
}

.feedback-button.confusing:hover:not(:disabled) {
  border-color: #6c757d;
  background-color: #e2e3e5;
}

.feedback-button.interesting:hover:not(:disabled) {
  border-color: #28a745;
  background-color: #d4edda;
}

.feedback-count {
  position: absolute;
  top: -8px;
  right: -8px;
  background-color: #4dc189;
  color: white;
  border-radius: 50%;
  padding: 2px 6px;
  font-size: 12px;
  min-width: 20px;
  text-align: center;
}

.cooldown-notice {
  margin-top: 15px;
  text-align: center;
  color: #666;
  font-size: 14px;
  padding: 8px;
  background-color: #f8f9fa;
  border-radius: 4px;
}
</style>
