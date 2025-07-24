<template>
  <div class="sub-dashboard-section">
    <h2>我的演讲</h2>
    <div v-if="loading" class="loading-state">
      <p>加载中...</p>
    </div>
    <div v-else-if="error" class="error-state">
      <p>{{ error }}</p>
      <button @click="fetchPresentations" class="retry-button">重试</button>
    </div>
    <div v-else-if="presentations.length === 0" class="empty-state">
      <p>您还未发布演讲，请先创建演讲。</p>
      <router-link to="/speaker/dashboard/create" class="create-link">创建新演讲</router-link>
    </div>
    <div v-else class="presentation-list">
      <div v-for="presentation in presentations" :key="presentation.id" class="presentation-item">
        <h3>{{ presentation.title }}</h3>
        <p>{{ presentation.description }}</p>
        <div class="action-buttons">
          <button @click="selectPresentation(presentation)" class="select-button">
            {{ selectedPresentationId === presentation.id ? '已选择' : '选择' }}
          </button>
          <button @click="manageFiles(presentation)" class="manage-button">文件管理</button>
          <button @click="manageQuizzes(presentation)" class="manage-button">题目管理</button>
          <button @click="viewStats(presentation)" class="manage-button">查看统计</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { getPresentations } from '../../services/presentation';
import { authState, getUserId, getUsername, debugAuthState } from '../../services/auth';

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
    // 打印当前认证状态，帮助调试
    debugAuthState('获取演讲列表前的认证状态');
    
    // 获取用户ID和用户名
    const userId = getUserId();
    const username = getUsername();
    
    // 调用API获取演讲列表
    const data = await getPresentations();
    console.log('获取演讲列表:', data);
    console.log('当前用户ID (authState):', authState.user?.id);
    console.log('当前用户ID (getUserId):', userId);
    console.log('当前用户名 (getUsername):', username);
    console.log('当前用户角色:', authState.user?.role);
    
    // 从localStorage直接获取userId进行比较
    const localStorageUserId = localStorage.getItem('userId');
    console.log('localStorage中的userId:', localStorageUserId);
    
    // 检查用户名和演讲列表
    if (!username) {
      // 如果没有用户名，按要求不显示任何演讲
      console.log('用户名不存在，按要求不显示演讲列表');
      presentations.value = [];
      error.value = '无法获取您的用户名，请重新登录';
    } else if (Array.isArray(data)) {
      // 手动在前端过滤出当前用户作为演讲者的演讲
      console.log('过滤演讲列表，只显示当前用户名为', username, '的演讲');
      
      // 记录原始数据以便调试
      if (data.length > 0) {
        console.log('原始数据:');
        data.forEach(p => console.log(`演讲ID ${p.id}, 标题: ${p.title}, 演讲者: ${p.speaker}`));
      } else {
        console.log('原始演讲列表为空');
      }
      
      // 检查数据结构
      if (data.length > 0) {
        console.log('数据示例:');
        console.log(JSON.stringify(data[0], null, 2));
      }
      
      // 基于演讲者字段过滤
      presentations.value = data.filter(p => {
        // 检查是否有speaker字段
        if (p.speaker === undefined) {
          console.log(`演讲ID ${p.id} 没有找到演讲者字段:`, p);
          return false;
        }
        
        // 将演讲者名称和当前用户名转换为小写进行不区分大小写的比较
        const speakerName = String(p.speaker).trim().toLowerCase();
        const currentUsername = String(username).trim().toLowerCase();
        
        // 比较
        const isMatch = speakerName === currentUsername;
        
        console.log(`演讲ID ${p.id}, 演讲者=${speakerName}, 当前用户=${currentUsername}, 匹配结果:`, isMatch);
        
        return isMatch;
      });
      
      console.log('过滤后的演讲列表包含', presentations.value.length, '个项目');
      
      // 如果过滤后没有演讲，保持空列表状态，前端会显示"您还未发布演讲"
      if (presentations.value.length === 0) {
        console.warn('过滤后没有找到匹配的演讲，保持空列表状态');
        
        // 记录当前用户名和所有演讲者名称，帮助调试
        console.log('当前用户名:', username);
        console.log('所有演讲者名称:', data.map(p => p.speaker));
        
        // 不再设置全部演讲，保持空列表
        presentations.value = [];
      }
    } else {
      // 如果返回的不是数组
      console.log('获取的数据不是数组:', data);
      presentations.value = [];
      error.value = '数据格式错误，请联系管理员';
    }
    
    console.log('最终的演讲列表:', presentations.value);
  } catch (err) {
    console.error('获取演讲列表失败:', err);
    error.value = err.message || '获取演讲列表失败，请稍后再试';
    presentations.value = [];
  } finally {
    loading.value = false;
  }
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

// 管理文件
const manageFiles = (presentation) => {
  selectPresentation(presentation); // 先选择这个演讲
  router.push('/speaker/dashboard/files');
};

// 管理测验
const manageQuizzes = (presentation) => {
  selectPresentation(presentation); // 先选择这个演讲
  router.push('/speaker/dashboard/quiz');
};

// 查看统计数据
const viewStats = (presentation) => {
  selectPresentation(presentation); // 先选择这个演讲
  router.push('/speaker/dashboard/stats');
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
}

.create-link, .retry-button {
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

.create-link:hover, .retry-button:hover {
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