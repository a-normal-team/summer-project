<template>
  <div class="sub-dashboard-section">
    <div class="live-quiz-status">
      <div class="header-section">
        <h2>实时答题状态</h2>
        <div class="quiz-meta">
          <span class="quiz-number">第 {{ currentQuizNumber }} 题</span>
          <span class="timer" v-if="timeLeft > 0">剩余 {{ timeLeft }} 秒</span>
        </div>
      </div>

      <div class="quiz-content">
        <div class="question-card">
          <p class="question">{{ currentQuiz.question }}</p>
          <div class="options-list">
            <div 
              v-for="option in currentQuiz.options" 
              :key="option.id"
              class="option-item"
              :class="{ 'correct': showResult && option.id === currentQuiz.correctAnswer }"
            >
              <div class="option-text">{{ option.text }}</div>
              <div class="option-stats">
                <div class="progress-bar" :style="{ width: getOptionPercentage(option.id) + '%' }"></div>
                <span class="count">{{ getOptionCount(option.id) }}</span>
                <span class="percentage">{{ getOptionPercentage(option.id) }}%</span>
              </div>
            </div>
          </div>
        </div>

        <div class="stats-cards">
          <div class="stat-card">
            <div class="stat-value">{{ totalResponses }}</div>
            <div class="stat-label">总答题人数</div>
          </div>
          <div class="stat-card">
            <div class="stat-value">{{ correctCount }}</div>
            <div class="stat-label">答对人数</div>
          </div>
          <div class="stat-card">
            <div class="stat-value">{{ correctRate }}%</div>
            <div class="stat-label">正确率</div>
          </div>
          <div class="stat-card">
            <div class="stat-value">{{ averageTime }}s</div>
            <div class="stat-label">平均用时</div>
          </div>
        </div>
      </div>

      <div class="action-section">
        <button 
          class="action-button"
          :class="{ 'danger': !showResult }"
          @click="toggleResult"
        >
          {{ showResult ? '隐藏答案' : '显示答案' }}
        </button>
        <button 
          class="action-button"
          @click="nextQuiz"
        >
          下一题
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';

const props = defineProps({
  currentQuiz: {
    type: Object,
    required: true
  },
  currentQuizNumber: {
    type: Number,
    required: true
  },
  responses: {
    type: Array,
    default: () => []
  },
  timeLeft: {
    type: Number,
    default: 0
  }
});

const showResult = ref(false);

const totalResponses = computed(() => props.responses.length);

const correctCount = computed(() => 
  props.responses.filter(r => r.answer === props.currentQuiz.correctAnswer).length
);

const correctRate = computed(() => 
  totalResponses.value > 0 
    ? Math.round((correctCount.value / totalResponses.value) * 100) 
    : 0
);

const averageTime = computed(() => {
  if (totalResponses.value === 0) return 0;
  const totalTime = props.responses.reduce((sum, r) => sum + r.timeSpent, 0);
  return Math.round(totalTime / totalResponses.value);
});

const getOptionCount = (optionId) => 
  props.responses.filter(r => r.answer === optionId).length;

const getOptionPercentage = (optionId) => {
  if (totalResponses.value === 0) return 0;
  return Math.round((getOptionCount(optionId) / totalResponses.value) * 100);
};

const toggleResult = () => {
  showResult.value = !showResult.value;
};

const nextQuiz = () => {
  // TODO: 实现下一题逻辑
  console.log('切换到下一题');
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

.live-quiz-status {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.header-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

h2 {
  color: #4dc189;
  margin: 0;
}

.quiz-meta {
  display: flex;
  gap: 20px;
  align-items: center;
}

.quiz-number {
  font-size: 18px;
  font-weight: bold;
  color: #333;
}

.timer {
  font-size: 18px;
  font-weight: bold;
  color: #dc3545;
}

.quiz-content {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.question-card {
  background-color: #f9f9f9;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.question {
  font-size: 16px;
  color: #333;
  margin-bottom: 20px;
  line-height: 1.5;
}

.options-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.option-item {
  background-color: #fff;
  border-radius: 6px;
  padding: 15px;
  border: 1px solid #eee;
}

.option-item.correct {
  border-color: #28a745;
  background-color: #d4edda;
}

.option-text {
  margin-bottom: 10px;
  color: #333;
}

.option-stats {
  position: relative;
  height: 24px;
  background-color: #eee;
  border-radius: 12px;
  overflow: hidden;
}

.progress-bar {
  position: absolute;
  left: 0;
  top: 0;
  height: 100%;
  background-color: #4dc189;
  transition: width 0.3s ease;
}

.count,
.percentage {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  color: #333;
  font-size: 12px;
  font-weight: bold;
  z-index: 1;
}

.count {
  left: 10px;
}

.percentage {
  right: 10px;
}

.stats-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 15px;
}

.stat-card {
  background-color: #fff;
  border-radius: 8px;
  padding: 20px;
  text-align: center;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.stat-value {
  font-size: 24px;
  font-weight: bold;
  color: #4dc189;
  margin-bottom: 5px;
}

.stat-label {
  font-size: 14px;
  color: #666;
}

.action-section {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
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
  border-color: #bb2d3b;
}
</style>
