<template>
  <div class="listener-presentation-container">
    <h2>参与演讲: {{ presentation.title }}</h2>
    <p>描述: {{ presentation.description }}</p>

    <div class="quiz-section" v-if="activeQuestion">
      <h3>当前题目</h3>
      <QuizModal :question="activeQuestion" @submit-answer="handleSubmitAnswer" />
    </div>
    <div v-else class="no-question">
      <p>等待演讲者发布题目...</p>
    </div>

    <div class="feedback-section">
      <h3>即时反馈</h3>
      <button @click="sendFeedback('讲得太快')">讲得太快</button>
      <button @click="sendFeedback('讲得太慢')">讲得太慢</button>
      <button @click="sendFeedback('内容乏味')">内容乏味</button>
      <button @click="sendFeedback('题目质量差')">题目质量差</button>
    </div>

    <button v-if="isPresentationEnded" @click="viewPersonalReport">查看个人报告</button>
    <button @click="router.back()">返回仪表盘</button>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import QuizModal from '@/components/QuizModal.vue'; // 假设QuizModal组件已创建
// import { io } from 'socket.io-client'; // 假设使用socket.io

const route = useRoute();
const router = useRouter();

interface ListenerPresentation {
  id: number | null;
  title: string;
  description: string;
}

const presentation = ref<ListenerPresentation>({
  id: null,
  title: '加载中...',
  description: '',
});

const activeQuestion = ref<{ id: number; text: string; options: string[]; type: string } | null>(null);
const isPresentationEnded = ref(false);

onMounted(() => {
  if (route.params.id) {
    presentation.value.id = Number(route.params.id);
    // 实际应用中，这里会调用API获取演讲详情
    console.log(`加载演讲参与数据: ${presentation.value.id}`);
    // 模拟加载数据
    presentation.value.title = 'Spring Boot入门';
    presentation.value.description = '这是一个关于Spring Boot的入门演讲。';

    // 模拟WebSocket连接和事件
    // const socket = io('http://localhost:5000');
    // socket.emit('join_presentation', { presentation_id: presentation.value.id });
    // socket.on('new_question', (data) => {
    //   activeQuestion.value = data;
    // });
    // socket.on('presentation_ended', () => {
    //   isPresentationEnded.value = true;
    // });
  }
});

const handleSubmitAnswer = (answer: string | string[]) => {
  alert(`提交答案: ${JSON.stringify(answer)}`);
  // 调用提交答案API
  // 模拟立即反馈
  alert('答案已提交！');
  activeQuestion.value = null; // 提交后隐藏题目
};

const sendFeedback = (feedbackType: string) => {
  alert(`发送反馈: ${feedbackType}`);
  // 调用发送反馈API
};

const viewPersonalReport = () => {
  alert('查看个人报告');
  router.push(`/listener/presentations/${presentation.value.id}/report`);
};
</script>

<style scoped>
.listener-presentation-container {
  max-width: 800px;
  margin: 50px auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  text-align: center;
}

h2 {
  color: #333;
  margin-bottom: 10px;
}

p {
  color: #666;
  margin-bottom: 20px;
}

.quiz-section, .feedback-section {
  background-color: #f9f9f9;
  border: 1px solid #eee;
  border-radius: 6px;
  padding: 15px;
  margin-bottom: 20px;
}

.no-question {
  padding: 30px;
  color: #999;
  font-style: italic;
}

.feedback-section button {
  background-color: #ffc107;
  color: #333;
  padding: 8px 12px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  margin: 5px;
}

.feedback-section button:hover {
  background-color: #e0a800;
}

button {
  background-color: #007bff;
  color: white;
  padding: 10px 15px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
  margin-top: 20px;
  margin-right: 10px;
}

button:last-of-type {
  background-color: #6c757d;
}

button:hover {
  opacity: 0.9;
}
</style>
