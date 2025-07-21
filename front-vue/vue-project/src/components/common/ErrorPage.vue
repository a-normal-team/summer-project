<template>
  <div class="sub-dashboard-section error-page">
    <div class="error-content">
      <h1>{{ code }}</h1>
      <h2>{{ title }}</h2>
      <p>{{ message }}</p>
      <button class="action-button" @click="goBack">返回上一页</button>
    </div>
  </div>
</template>

<script setup>
import { defineProps } from 'vue';
import { useRouter } from 'vue-router';

const props = defineProps({
  code: {
    type: String,
    default: '404'
  },
  title: {
    type: String,
    default: '页面未找到'
  },
  message: {
    type: String,
    default: '抱歉，您访问的页面不存在。'
  }
});

const router = useRouter();

const goBack = () => {
  router.back();
};
</script>

<style scoped>
.error-page {
  padding: 40px;
  text-align: center;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.error-content {
  max-width: 500px;
  margin: 0 auto;
}

h1 {
  font-size: 72px;
  color: #4dc189;
  margin-bottom: 20px;
}

h2 {
  color: #333;
  margin-bottom: 15px;
}

p {
  color: #666;
  margin-bottom: 30px;
  font-size: 16px;
  line-height: 1.5;
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

.action-button:hover {
  background-color: #3aa875;
  transform: translateY(-1px);
}
</style>
