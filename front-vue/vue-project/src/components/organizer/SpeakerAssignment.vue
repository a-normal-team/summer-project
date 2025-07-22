<template>
  <div class="sub-dashboard-section">
    <h2>演讲者分配</h2>
    
    <div v-if="!selectedPresentationId" class="no-selection">
      <p>请先在"所有演讲"中选择一个演讲进行操作</p>
    </div>
    
    <div v-else-if="loading" class="loading-state">
      <p>加载中...</p>
    </div>
    
    <div v-else-if="error" class="error-state">
      <p>{{ error }}</p>
      <button @click="fetchPresentationDetails" class="retry-button">重试</button>
    </div>
    
    <div v-else class="assignment-container">
      <div class="presentation-header">
        <h3>{{ presentationDetails?.title }}</h3>
        <p>当前演讲者: {{ presentationDetails?.speaker || '未分配' }}</p>
      </div>
      
      <div class="search-section">
        <div class="search-box">
          <input 
            type="text" 
            v-model="searchQuery"
            placeholder="搜索演讲者..."
          />
        </div>
      </div>

      <div v-if="speakers.length === 0" class="empty-state">
        <p>暂无可分配的演讲者</p>
      </div>
      
      <div v-else class="speakers-list">
        <div v-for="speaker in filteredSpeakers" :key="speaker.id" class="speaker-item">
          <div class="speaker-info">
            <h3>{{ speaker.username }}</h3>
            <p>{{ speaker.email }}</p>
          </div>
          
          <button 
            @click="assignSpeaker(speaker.id)" 
            class="assign-button"
            :disabled="assigning"
          >
            {{ assigning && assigningSpeakerId === speaker.id ? '分配中...' : '分配' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import { getPresentationById, assignSpeakerToPresentation } from '../../services/presentation';

// 状态变量
const selectedPresentationId = ref(null);
const presentationDetails = ref(null);
const speakers = ref([]);
const searchQuery = ref('');
const loading = ref(false);
const error = ref(null);
const assigning = ref(false);
const assigningSpeakerId = ref(null);

// 模拟数据 - 实际中应该从API获取
speakers.value = [
  { id: 1, username: 'speaker_one', email: 'speaker1@example.com' },
  { id: 2, username: 'speaker_two', email: 'speaker2@example.com' },
  { id: 3, username: 'speaker_three', email: 'speaker3@example.com' }
];

// 页面加载时获取已选择的演讲ID
onMounted(() => {
  const storedId = localStorage.getItem('selectedPresentationId');
  if (storedId) {
    selectedPresentationId.value = parseInt(storedId);
    fetchPresentationDetails();
    // fetchSpeakers(); // 实际项目中应该实现此函数获取所有演讲者
  }
});

// 监听选中的演讲ID变化
watch(selectedPresentationId, (newValue) => {
  if (newValue) {
    fetchPresentationDetails();
    // fetchSpeakers(); // 实际项目中应该实现此函数获取所有演讲者
  } else {
    presentationDetails.value = null;
  }
});

// 过滤演讲者
const filteredSpeakers = computed(() => {
  if (!searchQuery.value) return speakers.value;
  
  const query = searchQuery.value.toLowerCase();
  return speakers.value.filter(speaker => 
    speaker.username.toLowerCase().includes(query) ||
    speaker.email.toLowerCase().includes(query)
  );
});

// 获取演讲详情
const fetchPresentationDetails = async () => {
  if (!selectedPresentationId.value) return;
  
  try {
    loading.value = true;
    error.value = null;
    
    // 以organizer角色获取演讲详情
    const data = await getPresentationById(selectedPresentationId.value, 'organizer');
    presentationDetails.value = data;
  } catch (err) {
    console.error('获取演讲详情失败:', err);
    error.value = '获取演讲详情失败: ' + (err.message || '未知错误');
  } finally {
    loading.value = false;
  }
};

// 分配演讲者
const assignSpeaker = async (speakerId) => {
  if (!selectedPresentationId.value || !speakerId) return;
  
  try {
    assigning.value = true;
    assigningSpeakerId.value = speakerId;
    error.value = null;
    
    await assignSpeakerToPresentation(selectedPresentationId.value, speakerId);
    
    // 分配成功后重新获取演讲详情
    await fetchPresentationDetails();
    
    // 显示成功消息
    alert('演讲者分配成功');
  } catch (err) {
    console.error('分配演讲者失败:', err);
    error.value = '分配演讲者失败: ' + (err.message || '未知错误');
    alert('分配演讲者失败: ' + (err.message || '未知错误'));
  } finally {
    assigning.value = false;
    assigningSpeakerId.value = null;
  }
};
</script>

<style scoped>
.sub-dashboard-section {
  padding: 20px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  height: 100%;
  width: 100%;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  flex: 1;
  box-sizing: border-box;
  min-height: 0;
}

h2 {
  color: #4dc189;
  margin-bottom: 20px;
}

.no-selection, .empty-state, .loading-state, .error-state {
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

.presentation-header {
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 1px solid #eee;
}

.presentation-header h3 {
  color: #333;
  margin-bottom: 5px;
}

.search-section {
  margin-bottom: 20px;
}

.search-box {
  position: relative;
}

.search-box input {
  width: 100%;
  padding: 10px 15px;
  border: 1px solid #ddd;
  border-radius: 20px;
  font-size: 14px;
  outline: none;
  transition: border-color 0.3s ease;
}

.search-box input:focus {
  border-color: #4dc189;
}

.speakers-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.speaker-item {
  background-color: #f9f9f9;
  border: 1px solid #eee;
  border-radius: 8px;
  padding: 15px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.speaker-info h3 {
  margin: 0;
  color: #333;
  font-size: 16px;
}

.speaker-info p {
  margin: 5px 0 0;
  color: #666;
  font-size: 14px;
}

.assign-button {
  background-color: #4dc189;
  color: white;
  border: none;
  border-radius: 20px;
  padding: 8px 20px;
  font-size: 14px;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s ease;
}

.assign-button:hover:not(:disabled) {
  background-color: #3aa875;
  transform: translateY(-1px);
}

.assign-button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}
</style>
