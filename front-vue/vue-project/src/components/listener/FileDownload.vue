<template>
  <div class="sub-dashboard-section">
    <h2>文件下载</h2>
    
    <div v-if="loading" class="loading-state">
      <p>加载中...</p>
    </div>
    
    <div v-else-if="error" class="error-state">
      <p>{{ error }}</p>
      <button @click="fetchParticipatedPresentations" class="retry-button">重试</button>
    </div>
    
    <div v-else-if="presentations.length === 0" class="empty-state">
      <p>您还未参与任何演讲，暂无可下载的文件</p>
    </div>
    
    <div v-else>
      <div v-for="presentation in presentations" :key="presentation.id" class="presentation-section">
        <div class="presentation-header">
          <h3>{{ presentation.title }}</h3>
          <p>{{ presentation.description }}</p>
          <p>演讲者: {{ presentation.speaker || '未分配' }}</p>
        </div>
        
        <div v-if="!presentation.files || presentation.files.length === 0" class="empty-files">
          <p>该演讲暂无可下载的文件</p>
        </div>
        
        <div v-else class="files-list">
          <div v-for="file in presentation.files" :key="file.id" class="file-item">
            <div class="file-info">
              <p class="file-name">{{ file.filename }}</p>
              <p class="file-meta">{{ formatFileSize(file.size) }} - {{ formatDateTime(file.upload_date) }}</p>
            </div>
            <button @click="downloadFile(file.id)" class="manage-button">
              下载
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { getPresentations } from '../../services/presentation';
import { getFilesByPresentation, getFileDownloadUrl } from '../../services/file';
import { authState } from '../../services/auth';

// 状态变量
const presentations = ref([]);
const loading = ref(false);
const error = ref(null);

// 页面加载时获取参与过的演讲
onMounted(async () => {
  await fetchParticipatedPresentations();
});

// 获取参与过的演讲
const fetchParticipatedPresentations = async () => {
  if (!authState.isAuthenticated) {
    error.value = '请先登录';
    return;
  }
  
  loading.value = true;
  error.value = null;
  
  try {
    // 以listener角色获取参与过的演讲
    const data = await getPresentations('listener');
    
    if (Array.isArray(data)) {
      // 存储演讲信息，稍后添加文件信息
      const presentationsWithoutFiles = [...data];
      const presentationsWithFiles = [];
      
      // 为每个演讲获取关联的文件
      for (const presentation of presentationsWithoutFiles) {
        try {
          const files = await getFilesByPresentation(presentation.id);
          presentationsWithFiles.push({
            ...presentation,
            files: files || []
          });
        } catch (fileError) {
          console.error(`获取演讲(ID: ${presentation.id})的文件失败:`, fileError);
          presentationsWithFiles.push({
            ...presentation,
            files: []
          });
        }
      }
      
      presentations.value = presentationsWithFiles;
    } else {
      presentations.value = [];
      error.value = '数据格式错误，请联系管理员';
    }
  } catch (err) {
    console.error('获取参与的演讲列表失败:', err);
    error.value = err.message || '获取演讲列表失败，请稍后再试';
    presentations.value = [];
  } finally {
    loading.value = false;
  }
};

// 下载文件
const downloadFile = (fileId) => {
  try {
    // 获取文件下载URL
    const downloadUrl = getFileDownloadUrl(fileId);
    
    // 打开新窗口下载文件
    window.open(downloadUrl, '_blank');
    
    console.log(`下载文件ID: ${fileId}, URL: ${downloadUrl}`);
  } catch (err) {
    console.error('文件下载失败:', err);
    alert('文件下载失败: ' + (err.message || '未知错误'));
  }
};

// 格式化文件大小
const formatFileSize = (sizeInBytes) => {
  if (!sizeInBytes) return '未知大小';
  
  const units = ['B', 'KB', 'MB', 'GB', 'TB'];
  let size = sizeInBytes;
  let unitIndex = 0;
  
  while (size >= 1024 && unitIndex < units.length - 1) {
    size /= 1024;
    unitIndex++;
  }
  
  return `${size.toFixed(2)} ${units[unitIndex]}`;
};

// 格式化日期时间
const formatDateTime = (dateTimeStr) => {
  if (!dateTimeStr) return '未知';
  
  try {
    const date = new Date(dateTimeStr);
    return new Intl.DateTimeFormat('zh-CN', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit',
      hour12: false
    }).format(date);
  } catch (err) {
    return dateTimeStr;
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

h3 {
  color: #333;
  margin-bottom: 10px;
}

.loading-state, .error-state, .empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 50px 20px;
  text-align: center;
}

.error-state {
  color: #e74c3c;
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

.presentation-section {
  margin-bottom: 30px;
  padding: 15px;
  background-color: #f9f9f9;
  border-radius: 8px;
}

.presentation-header {
  margin-bottom: 15px;
  padding-bottom: 10px;
  border-bottom: 1px solid #eee;
}

.empty-files {
  padding: 20px;
  text-align: center;
  color: #666;
}

.files-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.file-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 15px;
  background-color: #fff;
  border: 1px solid #eee;
  border-radius: 6px;
}

.file-info {
  flex-grow: 1;
}

.file-name {
  font-weight: 500;
  color: #333;
  margin-bottom: 5px;
}

.file-meta {
  font-size: 12px;
  color: #666;
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
  min-width: 60px;
  text-align: center;
}

.manage-button:hover {
  background-color: #f0f9f6;
  transform: translateY(-1px);
}
</style>
