<template>
  <div class="sub-dashboard-section">
    <div class="speaker-assignment">
      <div class="header-section">
        <h2>演讲者分配</h2>
        <button class="action-button" @click="showInviteModal = true">
          邀请演讲者
        </button>
      </div>

      <div class="assignment-content">
        <div class="search-section">
          <div class="search-box">
            <input 
              type="text" 
              v-model="searchQuery"
              placeholder="搜索演讲者..."
            />
            <span class="search-icon">🔍</span>
          </div>
          <div class="filter-buttons">
            <button 
              v-for="status in filterStatus"
              :key="status.value"
              class="filter-button"
              :class="{ active: currentFilter === status.value }"
              @click="currentFilter = status.value"
            >
              {{ status.label }}
            </button>
          </div>
        </div>

        <div class="speakers-grid">
          <div 
            v-for="speaker in filteredSpeakers"
            :key="speaker.id"
            class="speaker-card"
          >
            <div class="speaker-info">
              <div class="avatar">
                {{ speaker.name.charAt(0) }}
              </div>
              <div class="details">
                <h3>{{ speaker.name }}</h3>
                <p class="email">{{ speaker.email }}</p>
                <div class="tags">
                  <span 
                    v-for="tag in speaker.tags"
                    :key="tag"
                    class="tag"
                  >
                    {{ tag }}
                  </span>
                </div>
              </div>
            </div>

            <div class="presentation-info">
              <div class="presentation-count">
                <span class="count">{{ speaker.presentationCount }}</span>
                <span class="label">演讲数</span>
              </div>
              <div class="status-badge" :class="speaker.status">
                {{ getStatusText(speaker.status) }}
              </div>
            </div>

            <div class="action-buttons">
              <button 
                class="action-button"
                @click="assignPresentation(speaker)"
              >
                分配演讲
              </button>
              <button 
                class="action-button secondary"
                @click="viewProfile(speaker)"
              >
                查看资料
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 邀请演讲者模态框 -->
    <div v-if="showInviteModal" class="modal-backdrop" @click="showInviteModal = false">
      <div class="modal-content" @click.stop>
        <h3>邀请演讲者</h3>
        <form @submit.prevent="sendInvite" class="invite-form">
          <div class="form-group">
            <label>邮箱地址</label>
            <input 
              type="email" 
              v-model="inviteEmail"
              placeholder="请输入邮箱地址"
              required
            />
          </div>
          <div class="form-group">
            <label>邀请消息</label>
            <textarea 
              v-model="inviteMessage"
              placeholder="请输入邀请消息"
              rows="4"
            ></textarea>
          </div>
          <div class="modal-actions">
            <button 
              type="button" 
              class="action-button secondary"
              @click="showInviteModal = false"
            >
              取消
            </button>
            <button 
              type="submit" 
              class="action-button"
            >
              发送邀请
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';

const searchQuery = ref('');
const currentFilter = ref('all');
const showInviteModal = ref(false);
const inviteEmail = ref('');
const inviteMessage = ref('');

const filterStatus = [
  { label: '全部', value: 'all' },
  { label: '活跃', value: 'active' },
  { label: '空闲', value: 'available' },
  { label: '已分配', value: 'assigned' }
];

// 模拟数据
const speakers = ref([
  {
    id: 1,
    name: '张教授',
    email: 'zhang@example.com',
    tags: ['人工智能', '机器学习'],
    presentationCount: 5,
    status: 'active'
  },
  {
    id: 2,
    name: '李博士',
    email: 'li@example.com',
    tags: ['Web开发', '前端技术'],
    presentationCount: 3,
    status: 'available'
  }
]);

const filteredSpeakers = computed(() => {
  return speakers.value
    .filter(speaker => {
      const matchesSearch = speaker.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
                          speaker.email.toLowerCase().includes(searchQuery.value.toLowerCase());
      const matchesFilter = currentFilter.value === 'all' || speaker.status === currentFilter.value;
      return matchesSearch && matchesFilter;
    });
});

const getStatusText = (status) => {
  const statusMap = {
    active: '进行中',
    available: '空闲',
    assigned: '已分配'
  };
  return statusMap[status] || status;
};

const assignPresentation = (speaker) => {
  // TODO: 实现分配演讲逻辑
  console.log('分配演讲给:', speaker);
};

const viewProfile = (speaker) => {
  // TODO: 实现查看资料逻辑
  console.log('查看资料:', speaker);
};

const sendInvite = () => {
  // TODO: 实现发送邀请逻辑
  console.log('发送邀请:', { email: inviteEmail.value, message: inviteMessage.value });
  showInviteModal.value = false;
  inviteEmail.value = '';
  inviteMessage.value = '';
};
</script>

<style scoped>
.speaker-assignment {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.header-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

h2 {
  color: #4dc189;
  margin: 0;
}

.search-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.search-box {
  position: relative;
  flex: 1;
  max-width: 300px;
}

.search-box input {
  width: 100%;
  padding: 10px 30px 10px 10px;
  border: 1px solid #ddd;
  border-radius: 20px;
  font-size: 14px;
}

.search-icon {
  position: absolute;
  right: 10px;
  top: 50%;
  transform: translateY(-50%);
  color: #666;
}

.filter-buttons {
  display: flex;
  gap: 10px;
}

.filter-button {
  padding: 6px 12px;
  border-radius: 15px;
  border: 1px solid #ddd;
  background-color: #fff;
  color: #666;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.filter-button:hover {
  border-color: #4dc189;
  color: #4dc189;
}

.filter-button.active {
  background-color: #4dc189;
  border-color: #4dc189;
  color: #fff;
}

.speakers-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.speaker-card {
  background-color: #f9f9f9;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.speaker-info {
  display: flex;
  gap: 15px;
}

.avatar {
  width: 50px;
  height: 50px;
  border-radius: 25px;
  background-color: #4dc189;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  font-weight: bold;
}

.details {
  flex: 1;
}

.details h3 {
  color: #333;
  margin: 0 0 5px 0;
  font-size: 16px;
}

.email {
  color: #666;
  font-size: 14px;
  margin-bottom: 10px;
}

.tags {
  display: flex;
  flex-wrap: wrap;
  gap: 5px;
}

.tag {
  padding: 2px 8px;
  background-color: #e9ecef;
  border-radius: 10px;
  font-size: 12px;
  color: #666;
}

.presentation-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 0;
  border-top: 1px solid #eee;
  border-bottom: 1px solid #eee;
}

.presentation-count {
  text-align: center;
}

.presentation-count .count {
  display: block;
  font-size: 24px;
  font-weight: bold;
  color: #4dc189;
}

.presentation-count .label {
  font-size: 12px;
  color: #666;
}

.status-badge {
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: bold;
  color: white;
}

.status-badge.active {
  background-color: #28a745;
}

.status-badge.available {
  background-color: #17a2b8;
}

.status-badge.assigned {
  background-color: #6c757d;
}

.action-buttons {
  display: flex;
  gap: 10px;
}

.action-button {
  flex: 1;
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

.action-button.secondary {
  background-color: #fff;
  color: #4dc189;
}

.action-button.secondary:hover {
  background-color: #f0f9f4;
}

/* 模态框样式 */
.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background-color: #fff;
  border-radius: 8px;
  padding: 20px;
  width: 90%;
  max-width: 500px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.modal-content h3 {
  color: #4dc189;
  margin-bottom: 20px;
}

.invite-form {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.form-group label {
  color: #333;
  font-weight: bold;
  font-size: 14px;
}

.form-group input,
.form-group textarea {
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 20px;
}
</style>
