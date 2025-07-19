<template>
  <div class="quiz-modal-overlay" @click.self="closeModal">
    <div class="quiz-modal-content">
      <h3>{{ question.text }}</h3>
      <div class="options">
        <div v-for="(option, index) in question.options" :key="index" class="option-item">
          <input
            :type="question.type === 'multiple-choice' ? 'checkbox' : 'radio'"
            :id="`option-${index}`"
            :value="option"
            v-model="selectedAnswer"
            :name="question.id.toString()"
          />
          <label :for="`option-${index}`">{{ String.fromCharCode(65 + index) }}. {{ option }}</label>
        </div>
      </div>
      <div class="timer">
        倒计时: {{ timeLeft }} 秒
      </div>
      <button @click="submitAnswer" :disabled="!selectedAnswer || timeLeft === 0">提交</button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, onMounted, onUnmounted } from 'vue';

const props = defineProps<{
  question: {
    id: number;
    text: string;
    options: string[];
    type: 'single-choice' | 'multiple-choice';
    duration?: number; // 题目持续时间，秒
  };
}>();

const emit = defineEmits(['submit-answer', 'close']);

const selectedAnswer = ref<string | string[] | null>(null);
const timeLeft = ref(props.question.duration || 10); // 默认10秒
let timer: number | undefined;

watch(
  () => props.question,
  (newQuestion) => {
    // 当题目变化时重置状态
    selectedAnswer.value = null;
    timeLeft.value = newQuestion.duration || 10;
    startTimer();
  },
  { immediate: true } // 立即执行一次，以便在组件挂载时启动计时器
);

const startTimer = () => {
  if (timer) clearInterval(timer);
  timer = setInterval(() => {
    if (timeLeft.value > 0) {
      timeLeft.value--;
    } else {
      clearInterval(timer);
      submitAnswer(); // 倒计时结束自动提交
    }
  }, 1000);
};

const submitAnswer = () => {
  if (selectedAnswer.value) {
    emit('submit-answer', selectedAnswer.value);
    closeModal();
  } else if (timeLeft.value === 0) {
    // 倒计时结束但未选择答案，提交空答案
    emit('submit-answer', null);
    closeModal();
  }
};

const closeModal = () => {
  if (timer) clearInterval(timer);
  emit('close');
};

onUnmounted(() => {
  if (timer) clearInterval(timer);
});
</script>

<style scoped>
.quiz-modal-overlay {
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

.quiz-modal-content {
  background-color: white;
  padding: 30px;
  border-radius: 8px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
  max-width: 500px;
  width: 90%;
  text-align: center;
}

h3 {
  color: #333;
  margin-bottom: 20px;
  font-size: 1.5em;
}

.options {
  margin-bottom: 20px;
  text-align: left;
}

.option-item {
  margin-bottom: 10px;
  display: flex;
  align-items: center;
}

.option-item input {
  margin-right: 10px;
  transform: scale(1.2);
}

.option-item label {
  font-size: 1.1em;
  color: #555;
  cursor: pointer;
}

.timer {
  font-size: 1.2em;
  color: #dc3545;
  font-weight: bold;
  margin-bottom: 20px;
}

button {
  background-color: #007bff;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1.1em;
}

button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

button:hover:not(:disabled) {
  background-color: #0056b3;
}
</style>
