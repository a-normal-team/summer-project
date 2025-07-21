<template>
  <div class="sub-dashboard-section">
    <h2>创建新演讲</h2>
    <form @submit.prevent="createPresentation">
      <div class="form-group">
        <label for="title">演讲标题:</label>
        <input type="text" id="title" v-model="presentation.title" required />
      </div>
      <div class="form-group">
        <label for="description">描述:</label>
        <textarea id="description" v-model="presentation.description"></textarea>
      </div>
      <button type="submit" class="submit-button">创建</button>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const presentation = ref({
  title: '',
  description: ''
});

const createPresentation = () => {
  // 实际应用中会调用后端 API
  console.log('创建演讲:', presentation.value);
  alert('演讲创建成功 (模拟)');
  // 清空表单
  presentation.value.title = '';
  presentation.value.description = '';
};
</script>

<style scoped>
.sub-dashboard-section {
  padding: 20px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

h2 {
  color: #4dc189;
  margin-bottom: 20px;
}

.form-group {
  margin-bottom: 15px;
}

label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
  color: #333;
}

input[type="text"],
textarea {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 5px;
  font-size: 16px;
  color: #333;
}

textarea {
  min-height: 100px;
  resize: vertical;
}

.submit-button {
  border-radius: 20px;
  border: 1px solid #4dc189;
  background-color: #4dc189;
  color: #FFFFFF;
  font-size: 12px;
  font-weight: bold;
  padding: 10px 20px;
  letter-spacing: 1px;
  text-transform: uppercase;
  transition: transform 80ms ease-in;
  cursor: pointer;
  margin-top: 10px;
}

.submit-button:active {
  transform: scale(0.95);
}
</style>
