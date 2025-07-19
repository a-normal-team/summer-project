<template>
  <div class="presentation-form-container">
    <h2>{{ isEditMode ? '编辑演讲' : '创建新演讲' }}</h2>
    <form @submit.prevent="handleSubmit">
      <div class="form-group">
        <label for="title">演讲标题:</label>
        <input type="text" id="title" v-model="presentation.title" required />
      </div>
      <div class="form-group">
        <label for="description">描述:</label>
        <textarea id="description" v-model="presentation.description"></textarea>
      </div>
      <div class="form-group">
        <label for="speaker">指派演讲者:</label>
        <select id="speaker" v-model="presentation.speakerId">
          <option v-for="speaker in speakers" :key="speaker.id" :value="speaker.id">
            {{ speaker.name }}
          </option>
        </select>
      </div>
      <button type="submit">{{ isEditMode ? '更新演讲' : '创建演讲' }}</button>
      <button type="button" @click="router.back()">取消</button>
    </form>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';

const route = useRoute();
const router = useRouter();

const isEditMode = ref(false);
interface Presentation {
  id: number | null;
  title: string;
  description: string;
  speakerId: number | null;
}

const presentation = ref<Presentation>({
  id: null,
  title: '',
  description: '',
  speakerId: null,
});

const speakers = ref([
  // 模拟演讲者数据
  { id: 1, name: '演讲者A' },
  { id: 2, name: '演讲者B' },
]);

onMounted(() => {
  if (route.params.id) {
    isEditMode.value = true;
    presentation.value.id = Number(route.params.id);
    // 实际应用中，这里会根据ID从API获取演讲详情并填充表单
    console.log(`加载演讲详情: ${presentation.value.id}`);
    // 模拟加载数据
    const existingPresentation = {
      id: 1,
      title: 'Spring Boot入门 (编辑)',
      description: '这是一个关于Spring Boot的入门演讲。',
      speakerId: 1,
    };
    presentation.value = { ...existingPresentation };
  }
});

const handleSubmit = () => {
  if (isEditMode.value) {
    alert(`更新演讲: ${JSON.stringify(presentation.value)}`);
    // 调用更新API
  } else {
    alert(`创建新演讲: ${JSON.stringify(presentation.value)}`);
    // 调用创建API
  }
  router.push('/organizer/dashboard'); // 提交后返回组织者仪表盘
};
</script>

<style scoped>
.presentation-form-container {
  max-width: 600px;
  margin: 50px auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.form-group {
  margin-bottom: 15px;
  text-align: left;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}

.form-group input[type="text"],
.form-group textarea,
.form-group select {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  box-sizing: border-box;
}

button {
  padding: 10px 15px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
  margin-right: 10px;
}

button[type="button"] {
  background-color: #6c757d;
}

button:hover {
  opacity: 0.9;
}
</style>
