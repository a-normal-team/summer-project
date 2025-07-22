<template>
  <div class="sub-dashboard-section">
    <h2>全部演讲</h2>
    <div v-if="loading" class="loading-state">
      <p>加载中...</p>
    </div>
    <div v-else-if="error" class="error-state">
      <p>{{ error }}</p>
      <button @click="fetchPresentations" class="retry-button">重试</button>
    </div>
    <div v-else-if="presentations.length === 0" class="empty-state">
      <p>暂无演讲记录</p>
    </div>
    <div v-else class="presentation-list">
      <div v-for="presentation in presentations" :key="presentation.id" class="presentation-item">
        <h3>{{ presentation.title }}</h3>
        <p>{{ presentation.description }}</p>
        <p>演讲者: {{ presentation.speaker || '未分配' }}</p>
        <p>状态: {{ getStatusText(presentation.status) }}</p>
        <div class="action-buttons">
          <button @click="selectPresentation(presentation)" class="select-button">
            {{ selectedPresentationId === presentation.id ? '已选择' : '选择' }}
          </button>
          <button @click="viewStats(presentation)" class="manage-button">整体统计</button>
          <button @click="viewListenerPerformance(presentation)" class="manage-button">听众表现</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { getPresentations } from '../../services/presentation';
import { authState } from '../../services/auth';

const router = useRouter();
const presentations = ref([]);
const selectedPresentationId = ref(null);
const loading = ref(false);
const error = ref(null);

// 页面加载时从API获取演讲列表
onMounted(async () => {
  // 从localStorage获取已选择的演讲ID
  const storedSelectedId = localStorage.getItem('selectedPresentationId');
  if (storedSelectedId) {
    selectedPresentationId.value = parseInt(storedSelectedId);
  }
  
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
    // 以organizer角色获取所有演讲列表
    const data = await getPresentations('organizer');
    console.log('获取所有演讲列表:', data);
    
    if (Array.isArray(data)) {
      presentations.value = data;
      console.log('展示所有演讲:', presentations.value.length, '个项目');
    } else {
      console.log('获取的数据不是数组:', data);
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

// 获取状态文本
const getStatusText = (status) => {
  const statusMap = {
    'pending': '计划中',
    'active': '进行中',
    'completed': '已完成'
  };
  return statusMap[status] || status || '未知';
};

// 选择演讲
const selectPresentation = (presentation) => {
  if (selectedPresentationId.value === presentation.id) {
    // 如果已经选择了这个演讲，则取消选择
    selectedPresentationId.value = null;
    localStorage.removeItem('selectedPresentationId');
  } else {
    // 选择这个演讲
    selectedPresentationId.value = presentation.id;
    localStorage.setItem('selectedPresentationId', presentation.id);
  }
};

// 查看统计数据
const viewStats = (presentation) => {
  selectPresentation(presentation); // 先选择这个演讲
  router.push('/organizer/dashboard/overall-stats');
};

// 查看听众表现
const viewListenerPerformance = (presentation) => {
  selectPresentation(presentation); // 先选择这个演讲
  router.push('/organizer/dashboard/listener-performance');
};
</script>

<style scoped>
.sub-dashboard-section {
  padding: 20px 20px 0 20px; /* 移除底部padding，避免双重padding影响 */
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

.create-button {
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
  margin-bottom: 20px;
}

.create-button:active {
  transform: scale(0.95);
}

.presentation-list {
  display: grid;
  gap: 20px;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  padding-bottom: 30px; /* 增加底部内边距确保最后一行完全可见 */
  margin-bottom: 20px; /* 额外的底部外边距 */
  flex: 1; /* 让列表在flex布局中占据可用空间 */
}

.presentation-item {
  background-color: #f9f9f9;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  display: flex;
  flex-direction: column;
  gap: 5px;
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

.presentation-item h3 {
  margin-top: 0;
  color: #333;
}

.manage-button {
  border-radius: 20px;
  border: 1px solid #3aa875;
  background-color: #ffffff;
  color: #3aa875;
  font-size: 11px;
  font-weight: bold;
  padding: 6px 10px;
  letter-spacing: 1px;
  text-transform: uppercase;
  transition: all 0.3s ease;
  cursor: pointer;
}

.manage-button:hover {
  background-color: #f0f9f6;
  transform: translateY(-1px);
}
</style>
