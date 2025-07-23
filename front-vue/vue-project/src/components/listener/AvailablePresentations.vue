<template>
  <div class="sub-dashboard-section">
    <h2>可参与的演讲</h2>
    
    <div v-if="loading" class="loading-state">
      <p>加载中...</p>
    </div>
    
    <div v-else-if="error" class="error-state">
      <p>{{ error }}</p>
      <button @click="fetchPresentations" class="retry-button">重试</button>
    </div>
    
    <div v-else-if="presentations.length === 0" class="empty-state">
      <p>暂无可参与的演讲</p>
    </div>
    
    <div v-else class="presentation-list">
      <div v-for="presentation in presentations" :key="presentation.id" class="presentation-item">
        <h3>{{ presentation.title }}</h3>
        <p>{{ presentation.description }}</p>
        <p>演讲者: {{ presentation.speaker || '未分配' }}</p>
        <div class="action-buttons">
          <button 
            @click="joinPresentation(presentation)" 
            class="select-button"
            :disabled="joiningPresentationId !== null"
            :class="{'loading': isJoining(presentation.id)}"
          >
            {{ isJoining(presentation.id) ? '加入中...' : '参与演讲' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { getPresentations, addListenerToPresentation } from '../../services/presentation';
import { authState } from '../../services/auth';

const router = useRouter();
const presentations = ref([]);
const loading = ref(false);
const error = ref(null);
const joiningPresentationId = ref(null); // 存储正在加入的演讲ID

// 判断演讲是否正在加入中
const isJoining = (presentationId) => joiningPresentationId.value === presentationId;

// 页面加载时从API获取演讲列表
onMounted(async () => {
  await fetchPresentations();
});

// 获取演讲列表
const fetchPresentations = async () => {
  if (!authState.isAuthenticated) {
    error.value = '请先登录';
    return;
  }
  
  loading.value = true;
  error.value = null;
  
  try {
    // 以listener角色获取所有演讲列表
    const data = await getPresentations('listener');
    
    if (Array.isArray(data)) {
      presentations.value = data;
    } else {
      presentations.value = [];
      error.value = '数据格式错误，请联系管理员';
    }
  } catch (err) {
    console.error('获取演讲列表失败:', err);
    error.value = err.message || '获取演讲列表失败，请稍后再试';
    presentations.value = [];
  } finally {
    loading.value = false;
  }
};

// 参与演讲
const joinPresentation = async (presentation) => {
  if (joiningPresentationId.value !== null) return; // 防止重复点击
  
  try {
    joiningPresentationId.value = presentation.id;
    error.value = null; // 清除之前的错误信息
    
    // 获取当前用户ID
    const currentUserId = authState.user?.id;
    if (!currentUserId) {
      error.value = '用户未登录或无法获取用户ID';
      joiningPresentationId.value = null;
      return;
    }
    
    // 调用API将听众添加到演讲
    const result = await addListenerToPresentation(presentation.id, currentUserId);
    console.log('加入演讲结果:', result);
    
    // 将选中的演讲信息存储在localStorage中
    localStorage.setItem('selectedPresentation', JSON.stringify({
      id: presentation.id,
      title: presentation.title
    }));
    
    // 导航到当前演讲页面
    router.push('/listener/dashboard/active');
  } catch (err) {
    console.error('加入演讲失败:', err);
    error.value = err.message || '加入演讲失败，请稍后重试';
  } finally {
    joiningPresentationId.value = null;
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
  box-sizing: border-box; /* 确保padding不会增加容器实际尺寸 */
  min-height: 0; /* 确保flex项可以正确计算overflow */
}

h2 {
  color: #4dc189;
  margin-bottom: 20px;
}

.presentation-list {
  display: grid;
  gap: 20px;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  padding-bottom: 30px; /* 增加底部内边距确保最后一行完全可见 */
  margin-bottom: 20px; /* 额外的底部外边距 */
}

.presentation-item {
  background-color: #f9f9f9;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.presentation-item h3 {
  color: #333;
  margin-bottom: 10px;
}

.presentation-item p {
  color: #666;
  margin-bottom: 8px;
  font-size: 14px;
}

.empty-state, .loading-state, .error-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 50px 20px;
  text-align: center;
}

.retry-button {
  margin-top: 15px;
  text-decoration: none;
  background-color: #4dc189;
  color: white;
  padding: 10px 20px;
  border-radius: 20px;
  font-weight: bold;
  transition: all 0.3s ease;
  border: none;
  cursor: pointer;
}

.retry-button:hover {
  background-color: #3aa875;
  transform: translateY(-1px);
}

.error-state {
  color: #e74c3c;
}

.action-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 10px;
}

.select-button {
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
  flex: 1;
}

.select-button:hover {
  background-color: #3aa875;
}

.select-button.loading {
  background-color: #90d5b8;
  cursor: not-allowed;
}

.select-button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}
</style>
