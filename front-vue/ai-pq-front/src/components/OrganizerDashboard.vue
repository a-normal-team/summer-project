<template>
  <div class="organizer-dashboard">
    <h2>组织者仪表盘</h2>
    <button @click="createPresentation">创建新演讲</button>
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
  { id: 1, title: 'Spring Boot入门', description: '...', speaker: '演讲者A', status: '进行中' },
  { id: 2, title: 'Vue 3 进阶', description: '...', speaker: '演讲者B', status: '已结束' },
]);

const createPresentation = () => {
  alert('跳转到创建新演讲页面/模态框');
  // router.push('/organizer/presentations/create');
};

const managePresentation = (id: number) => {
  alert(`跳转到演讲管理页面: ${id}`);
  // router.push(`/organizer/presentations/${id}/manage`);
};

onMounted(() => {
  // 实际应用中，这里会调用API获取演讲列表
  console.log('获取组织者演讲列表...');
});
</script>

<style scoped>
.organizer-dashboard {
  padding: 20px;
  text-align: left;
}

h2 {
  color: #333;
  margin-bottom: 20px;
}

button {
  background-color: #007bff;
  color: white;
  padding: 10px 15px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  margin-bottom: 20px;
}

button:hover {
  background-color: #0056b3;
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
