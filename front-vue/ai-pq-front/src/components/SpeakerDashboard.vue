<template>
  <div class="speaker-dashboard">
    <h2>演讲者仪表盘</h2>
    <h3>我的演讲</h3>
    <ul>
      <li v-for="presentation in presentations" :key="presentation.id">
        {{ presentation.title }} - {{ presentation.status }}
        <button @click="managePresentation(presentation.id)">管理</button>
      </li>
    </ul>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const presentations = ref([
  // 模拟数据
  { id: 1, title: 'Spring Boot入门', description: '...', status: '进行中' },
  { id: 2, title: 'Vue 3 进阶', description: '...', status: '已结束' },
]);

const managePresentation = (id: number) => {
  alert(`跳转到演讲详情/管理页面: ${id}`);
  // router.push(`/speaker/presentations/${id}`);
};

onMounted(() => {
  // 实际应用中，这里会调用API获取演讲列表
  console.log('获取演讲者演讲列表...');
});
</script>

<style scoped>
.speaker-dashboard {
  padding: 20px;
  text-align: left;
}

h2 {
  color: #333;
  margin-bottom: 20px;
}

ul {
  list-style: none;
  padding: 0;
}

li {
  background-color: #f9f9f9;
  border: 1px solid #ddd;
  padding: 10px;
  margin-bottom: 10px;
  border-radius: 4px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

li button {
  margin-bottom: 0;
  margin-left: 10px;
  padding: 5px 10px;
  background-color: #28a745;
}

li button:hover {
  background-color: #218838;
}
</style>
