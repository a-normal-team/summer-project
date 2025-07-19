<template>
  <div class="personal-report-container">
    <h2>个人报告 - {{ presentationTitle }}</h2>
    <div class="summary">
      <p>总题目数: {{ report.totalQuestions }}</p>
      <p>已答题目数: {{ report.answeredQuestions }}</p>
      <p>正确数: {{ report.correctAnswers }}</p>
      <p>正确率: {{ report.correctRate }}%</p>
      <p>排名: {{ report.rank }}</p>
    </div>

    <h3>题目详情</h3>
    <ul>
      <li v-for="question in report.questionDetails" :key="question.id" :class="{ correct: question.isCorrect, wrong: !question.isCorrect }">
        <p class="question-text">{{ question.text }}</p>
        <p>你的答案: {{ question.userAnswer }}</p>
        <p>正确答案: {{ question.correctAnswer }}</p>
        <p :class="question.isCorrect ? 'status-correct' : 'status-wrong'">
          {{ question.isCorrect ? '正确' : '错误' }}
        </p>
        <button @click="viewDiscussion(question.id)">进入讨论区</button>
      </li>
    </ul>

    <button @click="router.back()">返回演讲</button>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';

const route = useRoute();
const router = useRouter();

const presentationTitle = ref('加载中...');
const report = ref({
  totalQuestions: 0,
  answeredQuestions: 0,
  correctAnswers: 0,
  correctRate: 0,
  rank: 0,
  questionDetails: [
    // 模拟数据
    { id: 101, text: '什么是Spring Boot的核心特性？', userAnswer: '自动配置', correctAnswer: '自动配置', isCorrect: true },
    { id: 102, text: 'Vue 3中Composition API的优势是什么？', userAnswer: '更好的性能', correctAnswer: '更好的代码组织', isCorrect: false },
  ],
});

onMounted(() => {
  if (route.params.id) {
    const presentationId = Number(route.params.id);
    // 实际应用中，这里会调用API获取个人报告
    console.log(`加载个人报告数据: ${presentationId}`);
    // 模拟加载数据
    presentationTitle.value = 'Spring Boot入门';
    report.value.totalQuestions = 5;
    report.value.answeredQuestions = 5;
    report.value.correctAnswers = 4;
    report.value.correctRate = 80;
    report.value.rank = 1;
  }
});

const viewDiscussion = (questionId: number) => {
  alert(`进入题目讨论区: ${questionId}`);
  // router.push(`/discussion/questions/${questionId}`);
};
</script>

<style scoped>
.personal-report-container {
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
  margin-bottom: 20px;
}

.summary {
  background-color: #e7f3ff;
  border: 1px solid #b3d9ff;
  padding: 15px;
  border-radius: 6px;
  margin-bottom: 30px;
}

.summary p {
  margin: 5px 0;
  color: #333;
}

h3 {
  color: #555;
  margin-bottom: 15px;
  border-bottom: 1px solid #ddd;
  padding-bottom: 10px;
}

ul {
  list-style: none;
  padding: 0;
}

li {
  background-color: #f9f9f9;
  border: 1px solid #eee;
  padding: 15px;
  margin-bottom: 15px;
  border-radius: 6px;
  text-align: left;
}

li.correct {
  border-left: 5px solid #28a745;
}

li.wrong {
  border-left: 5px solid #dc3545;
}

.question-text {
  font-weight: bold;
  margin-bottom: 10px;
  color: #333;
}

.status-correct {
  color: #28a745;
  font-weight: bold;
}

.status-wrong {
  color: #dc3545;
  font-weight: bold;
}

li button {
  background-color: #17a2b8;
  color: white;
  padding: 8px 12px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  margin-top: 10px;
}

li button:hover {
  background-color: #138496;
}

.personal-report-container > button {
  background-color: #6c757d;
  color: white;
  padding: 10px 15px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
  margin-top: 20px;
}

.personal-report-container > button:hover {
  background-color: #5a6268;
}
</style>
