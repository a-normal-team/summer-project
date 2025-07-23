<template>
  <div class="sub-dashboard-section">
    <h2>文件管理</h2>
    <div v-if="loading" class="loading-state">
      <p>加载中...</p>
    </div>
    <div v-else-if="error" class="error-state">
      <p>{{ error }}</p>
      <button @click="checkSelectedPresentation" class="retry-button">重试</button>
    </div>
    <div v-else-if="!selectedPresentation" class="no-selection">
      <p>请先选择一个演讲</p>
      <router-link to="/speaker/dashboard/presentations" class="nav-link">选择演讲</router-link>
    </div>
    <div v-else>
      <div class="presentation-info">
        <h3>当前选中: {{ selectedPresentation.title }}</h3>
        <p>{{ selectedPresentation.description }}</p>
      </div>
      <button class="action-button upload-button" @click="uploadFile" :disabled="loading">上传文件</button>
      <div class="file-list" v-if="files.length > 0">
        <div class="file-item" v-for="file in files" :key="file.id">
          <div class="file-info">
            <p class="file-name">{{ file.filename }}</p>
            <p class="file-meta">上传时间：{{ new Date(file.upload_date).toLocaleString() }}</p>
            <p class="file-meta">大小：{{ Math.round(file.size / 1024) }} KB</p>
          </div>
          <div class="file-actions">
            <button class="action-button" @click="viewFile(file)">查看</button>
            <button class="action-button danger" @click="deleteFile(file)">删除</button>
          </div>
        </div>
      </div>
      <div v-else class="empty-files">
        <p>暂无文件，请上传文件</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { getPresentationById } from '../../services/presentation';
import { getFilesByPresentation, uploadFile as apiUploadFile, downloadFile as apiDownloadFile, deleteFile as apiDeleteFile } from '../../services/file';
import { authState } from '../../services/auth';

const router = useRouter();
const selectedPresentation = ref(null);
const files = ref([]);
const loading = ref(false);
const error = ref(null);

// 页面加载时检查是否有选中的演讲
onMounted(() => {
  checkSelectedPresentation();
});

// 检查是否有选中的演讲
const checkSelectedPresentation = async () => {
  const storedSelectedId = localStorage.getItem('selectedPresentationId');
  if (!storedSelectedId) return;

  loading.value = true;
  error.value = null;
  
  try {
    // 从API获取演讲详情
    const presentation = await getPresentationById(storedSelectedId);
    selectedPresentation.value = presentation;
    
    // 获取该演讲的文件
    await loadPresentationFiles(selectedPresentation.value.id);
  } catch (err) {
    console.error('获取演讲详情失败:', err);
    error.value = err.message || '获取演讲详情失败，请稍后再试';
  } finally {
    loading.value = false;
  }
};

// 加载演讲的文件
const loadPresentationFiles = async (presentationId) => {
  loading.value = true;
  error.value = null;
  
  try {
    // 从API获取文件列表
    const filesList = await getFilesByPresentation(presentationId);
    files.value = filesList || [];
  } catch (err) {
    console.error('获取文件列表失败:', err);
    error.value = err.message || '获取文件列表失败，请稍后再试';
    files.value = [];
  } finally {
    loading.value = false;
  }
};

// 上传文件
const uploadFile = () => {
  // 创建文件选择输入
  const fileInput = document.createElement('input');
  fileInput.type = 'file';
  
  // 监听文件选择事件
  fileInput.addEventListener('change', async (event) => {
    if (!event.target.files || event.target.files.length === 0) return;
    
    const file = event.target.files[0];
    loading.value = true;
    error.value = null;
    
    try {
      // 调用API上传文件
      const response = await apiUploadFile(file, selectedPresentation.value.id);
      console.log('文件上传成功:', response);
      
      // 重新加载文件列表
      await loadPresentationFiles(selectedPresentation.value.id);
    } catch (err) {
      console.error('文件上传失败:', err);
      error.value = err.message || '文件上传失败，请稍后再试';
    } finally {
      loading.value = false;
    }
  });
  
  // 触发文件选择对话框
  fileInput.click();
};

// 查看文件
const viewFile = async (file) => {
  try {
    loading.value = true;
    await apiDownloadFile(file.id);
  } catch (err) {
    console.error('文件查看失败:', err);
    error.value = err.message || '文件查看失败，请稍后再试';
  } finally {
    loading.value = false;
  }
};

// 删除文件
const deleteFile = async (file) => {
  // 确认是否要删除文件
  if (!confirm(`确定要删除文件 "${file.filename}" 吗？此操作不可撤销。`)) {
    return;
  }
  
  loading.value = true;
  error.value = null;
  
  try {
    // 调用API删除文件
    const result = await apiDeleteFile(file.id);
    console.log('文件删除成功:', result);
    
    // 从列表中移除已删除的文件
    files.value = files.value.filter(f => f.id !== file.id);
    
    // 显示成功消息
    alert(`文件 "${file.filename}" 已成功删除`);
  } catch (err) {
    console.error('文件删除失败:', err);
    error.value = err.message || '文件删除失败，请稍后再试';
    alert(`删除文件失败: ${err.message || '未知错误'}`);
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

.upload-button {
  margin-bottom: 20px;
  width: auto;
}

.file-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.no-selection, .empty-files, .loading-state, .error-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 30px 0;
}

.nav-link, .retry-button {
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

.nav-link:hover, .retry-button:hover {
  background-color: #3aa875;
  transform: translateY(-1px);
}

.error-state {
  color: #e74c3c;
}

.action-button:disabled {
  background-color: #a8d9c6;
  cursor: not-allowed;
  transform: none;
}

.presentation-info {
  background-color: #f9f9f9;
  padding: 15px;
  border-radius: 8px;
  margin-bottom: 20px;
  border-left: 4px solid #4dc189;
}

.presentation-info h3 {
  margin-top: 0;
  color: #333;
  margin-bottom: 5px;
}

.presentation-info p {
  margin: 0;
  color: #666;
}

.file-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #f9f9f9;
  padding: 15px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.file-info {
  flex-grow: 1;
}

.file-name {
  font-weight: bold;
  color: #333;
  margin-bottom: 5px;
}

.file-meta {
  font-size: 12px;
  color: #666;
}

.file-actions {
  display: flex;
  gap: 10px;
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

.action-button.danger {
  background-color: #dc3545;
  border-color: #dc3545;
}

.action-button.danger:hover {
  background-color: #bb2d3b;
}
</style>

