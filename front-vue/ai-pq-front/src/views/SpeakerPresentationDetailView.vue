<template>
  <div class="speaker-presentation-detail-container">
    <h2>演讲详情: {{ presentation.title }}</h2>
    <p>描述: {{ presentation.description }}</p>

    <div class="section">
      <h3>文件管理</h3>
      <input type="file" @change="handleFileUpload" />
      <button @click="uploadFile">上传文件</button>
      <ul>
        <li v-for="file in files" :key="file.id">
          {{ file.name }} ({{ file.size }} KB)
          <button @click="viewFileContent(file.id)">查看内容</button>
          <button @click="deleteFile(file.id)">删除</button>
        </li>
      </ul>
    </div>

    <div class="section">
      <h3>题目管理</h3>
      <button @click="generateQuiz">生成随堂测验</button>
      <div v-if="activeQuestion" class="active-question">
        <h4>当前活跃题目:</h4>
        <p>{{ activeQuestion.text }}</p>
        <ul>
          <li v-for="(option, index) in activeQuestion.options" :key="index">
            {{ String.fromCharCode(65 + index) }}. {{ option }}
          </li>
        </ul>
        <button @click="deactivateQuestion(activeQuestion.id)">结束当前题目</button>
      </div>
      <h3>历史题目</h3>
      <ul>
        <li v-for="question in historicalQuestions" :key="question.id">
          {{ question.text }}
          <button @click="viewQuestionStats(question.id)">查看统计</button>
          <button @click="viewDiscussion(question.id)">讨论区</button>
        </li>
      </ul>
    </div>

    <div class="section">
      <h3>实时统计 (当前题目)</h3>
      <p>作答人数: {{ currentQuestionStats.answeredCount }}</p>
      <p>正确率: {{ currentQuestionStats.correctRate }}%</p>
      <!-- 选项分布图表等 -->
    </div>

    <div class="section">
      <h3>即时反馈</h3>
      <ul>
        <li v-for="(count, feedbackType) in feedbackStats" :key="feedbackType">
          {{ feedbackType }}: {{ count }}
        </li>
      </ul>
    </div>

    <button @click="router.back()">返回仪表盘</button>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
// import { io } from 'socket.io-client'; // 假设使用socket.io

const route = useRoute();
const router = useRouter();

interface SpeakerPresentation {
  id: number | null;
  title: string;
  description: string;
}

const presentation = ref<SpeakerPresentation>({
  id: null,
  title: '加载中...',
  description: '',
});

const selectedFile = ref<File | null>(null);

const files = ref([
  // 模拟数据
  { id: 1, name: 'SpringBoot.pptx', size: 1024 },
  { id: 2, name: 'Vue3.pdf', size: 512 },
]);

const activeQuestion = ref<{ id: number; text: string; options: string[] } | null>(null);

const historicalQuestions = ref([
  // 模拟数据
  { id: 101, text: '什么是Spring Boot的核心特性？' },
  { id: 102, text: 'Vue 3中Composition API的优势是什么？' },
]);

const currentQuestionStats = ref({
  answeredCount: 0,
  correctRate: 0,
});

const feedbackStats = ref({
  '讲得太快': 0,
  '内容乏味': 0,
});

onMounted(() => {
  if (route.params.id) {
    presentation.value.id = Number(route.params.id);
    // 实际应用中，这里会调用API获取演讲详情、文件、题目和反馈
    console.log(`加载演讲详情数据: ${presentation.value.id}`);
    // 模拟加载数据
    presentation.value.title = 'Spring Boot入门';
    presentation.value.description = '这是一个关于Spring Boot的入门演讲。';

    // 模拟WebSocket连接和事件
    // const socket = io('http://localhost:5000');
    // socket.emit('join_presentation', { presentation_id: presentation.value.id });
    // socket.on('new_question', (data) => {
    //   activeQuestion.value = data;
    //   currentQuestionStats.value = { answeredCount: 0, correctRate: 0 }; // 重置统计
    // });
    // socket.on('question_stats_update', (data) => {
    //   currentQuestionStats.value = data;
    // });
    // socket.on('feedback_update', (data) => {
    //   feedbackStats.value = data;
    // });
  }
});

const handleFileUpload = (event: Event) => {
  const target = event.target as HTMLInputElement;
  if (target.files && target.files.length > 0) {
    selectedFile.value = target.files[0];
  }
};

const uploadFile = () => {
  if (selectedFile.value) {
    alert(`上传文件: ${selectedFile.value.name}`);
    // 调用文件上传API
  } else {
    alert('请选择一个文件');
  }
};

const viewFileContent = (fileId: number) => {
  alert(`查看文件内容: ${fileId}`);
  // 调用API获取文件内容
};

const deleteFile = (fileId: number) => {
  if (confirm(`确定要删除文件 ${fileId} 吗？`)) {
    alert(`删除文件: ${fileId}`);
    // 调用删除文件API
  }
};

const generateQuiz = () => {
  alert('生成随堂测验');
  // 调用生成题目API
  // 模拟生成题目
  activeQuestion.value = {
    id: 201,
    text: '以下哪个不是Spring Boot的特点？',
    options: ['内嵌Tomcat', '简化配置', '代码生成器', '自动配置'],
  };
};

const deactivateQuestion = (questionId: number) => {
  alert(`结束当前题目: ${questionId}`);
  // 调用结束题目API
  historicalQuestions.value.unshift({ id: questionId, text: activeQuestion.value!.text });
  activeQuestion.value = null;
};

const viewQuestionStats = (questionId: number) => {
  alert(`查看题目统计: ${questionId}`);
  // router.push(`/speaker/quiz/questions/${questionId}/stats`);
};

const viewDiscussion = (questionId: number) => {
  alert(`进入题目讨论区: ${questionId}`);
  // router.push(`/discussion/questions/${questionId}`);
};
</script>

<style scoped>
.speaker-presentation-detail-container {
  max-width: 900px;
  margin: 50px auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  text-align: left;
}

h2 {
  color: #333;
  margin-bottom: 10px;
  text-align: center;
}

p {
  color: #666;
  margin-bottom: 20px;
  text-align: center;
}

.section {
  background-color: #f9f9f9;
  border: 1px solid #eee;
  border-radius: 6px;
  padding: 15px;
  margin-bottom: 20px;
}

.section h3 {
  color: #555;
  margin-top: 0;
  margin-bottom: 15px;
  border-bottom: 1px solid #ddd;
  padding-bottom: 10px;
}

.section input[type="file"] {
  margin-right: 10px;
}

.section button {
  background-color: #28a745;
  color: white;
  padding: 8px 12px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  margin-right: 10px;
}

.section button:hover {
  background-color: #218838;
}

.section ul {
  list-style: none;
  padding: 0;
  margin-top: 15px;
}

.section li {
  padding: 8px 0;
  border-bottom: 1px dashed #eee;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.section li:last-child {
  border-bottom: none;
}

.section li button {
  background-color: #17a2b8;
  margin-left: 10px;
}

.section li button:last-of-type {
  background-color: #dc3545;
}

.active-question {
  background-color: #e7f3ff;
  border: 1px solid #b3d9ff;
  padding: 15px;
  border-radius: 6px;
  margin-top: 20px;
}

.active-question h4 {
  margin-top: 0;
  color: #007bff;
}

.active-question ul {
  margin-top: 10px;
}

.active-question li {
  border-bottom: none;
  padding: 5px 0;
}

.active-question button {
  background-color: #ffc107;
  color: #333;
  margin-top: 15px;
}

.speaker-presentation-detail-container > button {
  display: block;
  width: 150px;
  margin: 30px auto 0;
  background-color: #6c757d;
  color: white;
  padding: 10px 15px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
}

.speaker-presentation-detail-container > button:hover {
  background-color: #5a6268;
}
</style>
