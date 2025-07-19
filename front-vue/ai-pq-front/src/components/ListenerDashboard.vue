<template>
  <div class="listener-dashboard">
    <h2>听众仪表盘</h2>
    <h3>可参与的演讲</h3>
    <ul>
      <li v-for="presentation in presentations" :key="presentation.id">
        {{ presentation.title }} - 演讲者: {{ presentation.speaker }}
        <button @click="joinPresentation(presentation.id)">参与</button>
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
  { id: 1, title: 'Spring Boot入门', description: '...', speaker: '演讲者A' },
  { id: 2, title: 'Vue 3 进阶', description: '...', speaker: '演讲者B' },
]);

const joinPresentation = (id: number) => {
  alert(`跳转到演讲参与页面: ${id}`);
  // router.push(`/listener/presentations/${id}`);
};

onMounted(() => {
  // 实际应用中，这里会调用API获取可参与的演讲列表
  console.log('获取听众可参与的演讲列表...');
});
</script>

<style scoped>
.listener-dashboard {
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
  background-color: #007bff;
}

li button:hover {
  background-color: #0056b3;
}
</style>
