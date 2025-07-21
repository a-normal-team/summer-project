<template>
  <div v-if="show" class="modal-backdrop" @click.self="closeModal">
    <div class="modal-content">
      <div class="modal-header">
        <h2>答题结果</h2>
        <div class="result-badge" :class="{ 'correct': isCorrect }">
          {{ isCorrect ? '答对了' : '答错了' }}
        </div>
      </div>

      <div class="quiz-content">
        <div class="question-section">
          <h3>题目</h3>
          <p class="question">{{ quiz.question }}</p>
        </div>

        <div class="options-section">
          <div 
            v-for="option in quiz.options" 
            :key="option.id"
            class="option-item"
            :class="{
              'selected': option.id === selectedAnswer,
              'correct': option.id === quiz.correctAnswer,
              'incorrect': option.id === selectedAnswer && option.id !== quiz.correctAnswer
            }"
          >
            {{ option.text }}
          </div>
        </div>

        <div class="stats-section">
          <div class="stat-item">
            <span class="stat-label">用时</span>
            <span class="stat-value">{{ answerTime }}秒</span>
          </div>
          <div class="stat-item">
            <span class="stat-label">正确率</span>
            <span class="stat-value">{{ correctRate }}%</span>
          </div>
        </div>

        <div v-if="quiz.explanation" class="explanation-section">
          <h3>解释</h3>
          <p>{{ quiz.explanation }}</p>
        </div>
      </div>

      <div class="modal-footer">
        <button class="action-button" @click="viewDiscussion">
          查看讨论
        </button>
        <button class="action-button secondary" @click="closeModal">
          关闭
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineProps, defineEmits, computed } from 'vue';

const props = defineProps({
  show: Boolean,
  quiz: Object,
  selectedAnswer: String,
  answerTime: Number,
  correctRate: Number
});

const emit = defineEmits(['close', 'view-discussion']);

const isCorrect = computed(() => {
  return props.selectedAnswer === props.quiz?.correctAnswer;
});

const closeModal = () => {
  emit('close');
};

const viewDiscussion = () => {
  emit('view-discussion');
};
</script>

<style scoped>
.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background-color: white;
  border-radius: 8px;
  padding: 20px;
  width: 90%;
  max-width: 600px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.modal-header h2 {
  color: #4dc189;
  margin: 0;
}

.result-badge {
  padding: 6px 12px;
  border-radius: 15px;
  font-size: 14px;
  font-weight: bold;
  color: white;
  background-color: #dc3545;
}

.result-badge.correct {
  background-color: #28a745;
}

.question-section {
  margin-bottom: 20px;
}

.question-section h3 {
  color: #333;
  margin-bottom: 10px;
}

.question {
  color: #333;
  font-size: 16px;
  line-height: 1.5;
}

.options-section {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-bottom: 20px;
}

.option-item {
  padding: 12px 15px;
  border-radius: 6px;
  background-color: #f9f9f9;
  border: 1px solid #ddd;
  color: #333;
}

.option-item.selected {
  border-color: #4dc189;
}

.option-item.correct {
  background-color: #d4edda;
  border-color: #28a745;
  color: #155724;
}

.option-item.incorrect {
  background-color: #f8d7da;
  border-color: #dc3545;
  color: #721c24;
}

.stats-section {
  display: flex;
  gap: 20px;
  margin-bottom: 20px;
  padding: 15px;
  background-color: #f8f9fa;
  border-radius: 6px;
}

.stat-item {
  flex: 1;
  text-align: center;
}

.stat-label {
  display: block;
  color: #666;
  font-size: 14px;
  margin-bottom: 5px;
}

.stat-value {
  display: block;
  color: #333;
  font-size: 18px;
  font-weight: bold;
}

.explanation-section {
  background-color: #f9f9f9;
  border-radius: 6px;
  padding: 15px;
  margin-bottom: 20px;
}

.explanation-section h3 {
  color: #4dc189;
  margin-bottom: 10px;
}

.explanation-section p {
  color: #666;
  line-height: 1.5;
  font-size: 14px;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 20px;
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

.action-button.secondary {
  background-color: #6c757d;
  border-color: #6c757d;
}

.action-button.secondary:hover {
  background-color: #5a6268;
  border-color: #545b62;
}

/* 滚动条样式 */
.modal-content::-webkit-scrollbar {
  width: 6px;
}

.modal-content::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

.modal-content::-webkit-scrollbar-thumb {
  background: #4dc189;
  border-radius: 3px;
}

.modal-content::-webkit-scrollbar-thumb:hover {
  background: #3aa875;
}
</style>
