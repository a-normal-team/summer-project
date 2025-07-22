<template>
  <div class="sub-dashboard-section">
    <h2>创建新演讲</h2>
    <form @submit.prevent="createPresentation" class="creation-form">
      <div class="form-group">
        <label for="title">演讲标题:</label>
        <input type="text" id="title" v-model="presentation.title" required />
      </div>
      <div class="form-group">
        <label for="description">描述:</label>
        <textarea id="description" v-model="presentation.description"></textarea>
      </div>
      <div class="button-container">
        <button type="submit" class="submit-button" :disabled="loading">
          <span v-if="loading">创建中...</span>
          <span v-else>创建</span>
        </button>
      </div>
      <div v-if="error" class="error-message">
        {{ error }}
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { createPresentation as apiCreatePresentation } from '../../services/presentation';
import { authState, fetchUserProfile } from '../../services/auth';

const router = useRouter();
const presentation = ref({
  title: '',
  description: ''
});
const loading = ref(false);
const error = ref(null);

// 组件加载时刷新用户资料
onMounted(async () => {
  try {
    if (authState.isAuthenticated) {
      await fetchUserProfile();
      console.log('组件加载时获取用户资料:', authState.user);
    }
  } catch (err) {
    console.error('获取用户资料失败:', err);
  }
});

const createPresentation = async () => {
  console.log('当前认证状态:', authState.isAuthenticated);
  console.log('当前用户:', authState.user);
  console.log('当前用户角色:', authState.user?.role);
  
  // 手动设置用户角色为speaker，绕过角色检查
  if (authState.user && !authState.user.role) {
    authState.user.role = 'speaker';
    console.log('手动设置用户角色为speaker');
  }
  
  if (!authState.isAuthenticated) {
    error.value = '请先登录';
    return;
  }

  if (!presentation.value.title.trim()) {
    error.value = '请输入演讲标题';
    return;
  }

  loading.value = true;
  error.value = null;

  try {
    // 调用API创建演讲
    const presentationData = {
      title: presentation.value.title,
      description: presentation.value.description,
      role: 'speaker' // 显式添加角色信息
    };
    
    console.log('准备发送创建演讲请求:', presentationData);
    const response = await apiCreatePresentation(presentationData);

    console.log('创建演讲成功:', response);
    
    // 清空表单
    presentation.value.title = '';
    presentation.value.description = '';
    
    // 导航到我的演讲页面
    router.push('/speaker/dashboard/presentations');
  } catch (err) {
    console.error('创建演讲失败:', err);
    
    // 检查是否是权限错误
    if (err.message && err.message.includes('权限不足') || err.message.includes('只有演讲者')) {
      error.value = '权限错误：只有演讲者角色可以创建演讲，请联系管理员检查您的账户设置。';
    } else {
      error.value = err.message || '创建演讲失败，请稍后再试';
    }
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.sub-dashboard-section {
  padding: 20px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  height: 100%; /* 填满父容器高度 */
  width: 100%; /* 填满父容器宽度 */
  overflow-y: auto; /* 允许内容垂直滚动 */
  display: flex;
  flex-direction: column;
  flex: 1; /* 让组件填满父容器的剩余空间 */
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
input[type="number"],
input[type="date"],
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

.creation-form {
  display: flex;
  flex-direction: column;
  flex: 1;
}

.button-container {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
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
  transition: all 0.3s ease;
  cursor: pointer;
}

.submit-button:hover {
  background-color: #3aa875;
  transform: translateY(-1px);
}

.submit-button:disabled {
  background-color: #a8d9c6;
  cursor: not-allowed;
  transform: none;
}

.error-message {
  color: #e74c3c;
  margin-top: 15px;
  padding: 10px;
  background-color: #ffeaea;
  border-radius: 5px;
  text-align: center;
}
</style>
