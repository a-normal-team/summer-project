<template>
  <div class="modal-backdrop" v-if="show" @click.self="closeModal">
    <div class="modal-content">
      <div class="modal-header">
        <h2>{{ title }}</h2>
        <div class="timer" v-if="showTimer">{{ timeLeft }}秒</div>
      </div>
      <div class="quiz-content">
        <p class="question">{{ question }}</p>
        <div class="options">
          <button 
            v-for="option in options" 
            :key="option.id"
            class="option-button"
            :class="{ 
              'selected': selectedOption === option.id,
              'correct': showResult && option.id === correctAnswer,
              'incorrect': showResult && selectedOption === option.id && option.id !== correctAnswer
            }"
            @click="selectOption(option.id)"
            :disabled="showResult"
          >
            {{ option.text }}
          </button>
        </div>
      </div>
      <div class="modal-footer">
        <button 
          class="action-button submit-button" 
          @click="submitAnswer"
          :disabled="!selectedOption || showResult"
        >
          提交答案
        </button>
        <button 
          v-if="showResult" 
          class="action-button close-button"
          @click="closeModal"
        >
          关闭
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineProps, defineEmits, ref, onMounted, onUnmounted, watch } from 'vue';

const props = defineProps({
  show: Boolean,
  title: {
    type: String,
    default: '随堂测验'
  },
  question: String,
  options: Array,
  timeLimit: {
    type: Number,
    default: 30
  },
  correctAnswer: String,
  showTimer: {
    type: Boolean,
    default: true
  }
});

const emit = defineEmits(['close', 'submit']);

const selectedOption = ref(null);
const showResult = ref(false);
const timeLeft = ref(props.timeLimit);
let timer = null;

const selectOption = (optionId) => {
  selectedOption.value = optionId;
};

const submitAnswer = () => {
  if (selectedOption.value) {
    showResult.value = true;
    emit('submit', {
      selectedOption: selectedOption.value,
      correct: selectedOption.value === props.correctAnswer
    });
    clearInterval(timer);
  }
};

const closeModal = () => {
  emit('close');
  selectedOption.value = null;
  showResult.value = false;
  timeLeft.value = props.timeLimit;
  clearInterval(timer);
};

watch(() => props.show, (newValue) => {
  if (newValue && props.showTimer) {
    timeLeft.value = props.timeLimit;
    timer = setInterval(() => {
      if (timeLeft.value > 0) {
        timeLeft.value--;
      } else {
        submitAnswer();
      }
    }, 1000);
  }
});

onUnmounted(() => {
  if (timer) {
    clearInterval(timer);
  }
});
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

.timer {
  font-size: 18px;
  font-weight: bold;
  color: #4dc189;
}

.quiz-content {
  margin-bottom: 20px;
}

.question {
  font-size: 16px;
  color: #333;
  margin-bottom: 20px;
  line-height: 1.5;
}

.options {
  display: grid;
  gap: 10px;
}

.option-button {
  border: 1px solid #4dc189;
  background-color: #fff;
  color: #4dc189;
  padding: 12px 20px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  text-align: left;
}

.option-button:hover:not(:disabled) {
  background-color: #f0f9f4;
}

.option-button.selected {
  background-color: #4dc189;
  color: white;
}

.option-button.correct {
  background-color: #28a745;
  color: white;
  border-color: #28a745;
}

.option-button.incorrect {
  background-color: #dc3545;
  color: white;
  border-color: #dc3545;
}

.option-button:disabled {
  cursor: default;
  opacity: 0.7;
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

.action-button:hover:not(:disabled) {
  background-color: #3aa875;
  transform: translateY(-1px);
}

.action-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.submit-button {
  min-width: 120px;
}

.close-button {
  background-color: #6c757d;
  border-color: #6c757d;
}

.close-button:hover {
  background-color: #5a6268;
  border-color: #5a6268;
}
</style>
