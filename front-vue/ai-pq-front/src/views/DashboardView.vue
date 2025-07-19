<template>
  <div class="dashboard-container">
    <component :is="currentDashboardComponent" v-if="currentDashboardComponent" />
    <p v-else>加载中...</p>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, shallowRef } from 'vue';
import { useRouter } from 'vue-router';
import OrganizerDashboard from '@/components/OrganizerDashboard.vue';
import SpeakerDashboard from '@/components/SpeakerDashboard.vue';
import ListenerDashboard from '@/components/ListenerDashboard.vue';

const router = useRouter();
const userRole = ref(''); // 假设从认证状态中获取用户角色
import type { Component } from 'vue';
const currentDashboardComponent = shallowRef<Component | null>(null);

onMounted(() => {
  // 模拟获取用户角色，实际应用中会从后端获取或状态管理中读取
  // 为了演示，这里可以手动设置一个角色进行测试
  userRole.value = 'organizer'; // 可以改为 'speaker' 或 'listener' 进行测试

  switch (userRole.value) {
    case 'organizer':
      currentDashboardComponent.value = OrganizerDashboard;
      break;
    case 'speaker':
      currentDashboardComponent.value = SpeakerDashboard;
      break;
    case 'listener':
      currentDashboardComponent.value = ListenerDashboard;
      break;
    default:
      // 如果没有角色或角色无效，可以跳转到登录页或显示错误
      router.push('/login');
      break;
  }
});
</script>

<style scoped>
.dashboard-container {
  max-width: 800px;
  margin: 50px auto;
  padding: 20px;
  border: 1px solid #eee;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  text-align: center;
}

h1 {
  color: #333;
  margin-bottom: 20px;
}

p {
  color: #666;
}
</style>
