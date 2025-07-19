<template>
  <div class="presentation-manage-container">
    <h2>演讲管理: {{ presentation.title }}</h2>
    <div class="actions">
      <button @click="editPresentation">编辑演讲</button>
      <button @click="deletePresentation">删除演讲</button>
    </div>

    <div class="section">
      <h3>整体统计</h3>
      <p>参与人数: {{ overallStats.participants }}</p>
      <p>平均正确率: {{ overallStats.averageCorrectRate }}%</p>
    </div>

    <div class="section">
      <h3>听众表现</h3>
      <ul>
        <li v-for="listener in overallStats.listenerPerformance" :key="listener.id">
          {{ listener.name }} - 答对: {{ listener.correctAnswers }}/{{ listener.totalQuestions }} ({{ listener.correctRate }}%)
          <button @click="viewListenerReport(listener.id)">查看报告</button>
        </li>
      </ul>
    </div>

    <div class="section">
      <h3>文件列表</h3>
      <ul>
        <li v-for="file in files" :key="file.id">
          {{ file.name }} ({{ file.size }} KB)
          <button @click="downloadFile(file.id)">下载</button>
        </li>
      </ul>
    </div>

    <div class="section">
      <h3>反馈统计</h3>
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

const route = useRoute();
const router = useRouter();

interface PresentationDetails {
  id: number | null;
  title: string;
  description: string;
  speaker: string;
}

const presentation = ref<PresentationDetails>({
  id: null,
  title: '加载中...',
  description: '',
  speaker: '',
});

const overallStats = ref({
  participants: 0,
  averageCorrectRate: 0,
  listenerPerformance: [
    // 模拟数据
    { id: 1, name: '听众A', correctAnswers: 8, totalQuestions: 10, correctRate: 80 },
    { id: 2, name: '听众B', correctAnswers: 6, totalQuestions: 10, correctRate: 60 },
  ],
});

const files = ref([
  // 模拟数据
  { id: 1, name: 'SpringBoot.pptx', size: 1024 },
  { id: 2, name: 'Vue3.pdf', size: 512 },
]);

const feedbackStats = ref({
  '讲得太快': 5,
  '内容乏味': 2,
});

onMounted(() => {
  if (route.params.id) {
    presentation.value.id = Number(route.params.id);
    // 实际应用中，这里会调用API获取演讲详情、统计、文件和反馈
    console.log(`加载演讲管理数据: ${presentation.value.id}`);
    // 模拟加载数据
    presentation.value.title = 'Spring Boot入门';
    overallStats.value.participants = 10;
    overallStats.value.averageCorrectRate = 75;
  }
});

const editPresentation = () => {
  alert(`编辑演讲: ${presentation.value.id}`);
  router.push(`/organizer/presentations/${presentation.value.id}/edit`);
};

const deletePresentation = () => {
  if (confirm(`确定要删除演讲 "${presentation.value.title}" 吗？`)) {
    alert(`删除演讲: ${presentation.value.id}`);
    // 调用删除API
    router.push('/organizer/dashboard'); // 删除后返回仪表盘
  }
};

const viewListenerReport = (listenerId: number) => {
  alert(`查看听众 ${listenerId} 的报告`);
  // router.push(`/listener/presentations/${presentation.value.id}/report/${listenerId}`);
};

const downloadFile = (fileId: number) => {
  alert(`下载文件: ${fileId}`);
  // 调用下载API
};
</script>

<style scoped>
.presentation-manage-container {
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
  margin-bottom: 20px;
  text-align: center;
}

.actions {
  text-align: center;
  margin-bottom: 30px;
}

.actions button {
  padding: 10px 15px;
  margin: 0 10px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
}

.actions button:first-of-type {
  background-color: #ffc107;
  color: #333;
}

.actions button:first-of-type:hover {
  background-color: #e0a800;
}

.actions button:last-of-type {
  background-color: #dc3545;
  color: white;
}

.actions button:last-of-type:hover {
  background-color: #c82333;
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

.section ul {
  list-style: none;
  padding: 0;
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
  color: white;
  padding: 5px 10px;
  border: none;
  border-radius: 3px;
  cursor: pointer;
  font-size: 14px;
}

.section li button:hover {
  background-color: #138496;
}

.presentation-manage-container > button {
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

.presentation-manage-container > button:hover {
  background-color: #5a6268;
}
</style>
