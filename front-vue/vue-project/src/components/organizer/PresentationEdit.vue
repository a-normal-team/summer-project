<template>
  <div class="sub-dashboard-section">
    <div class="presentation-edit">
      <div class="header-section">
        <h2>{{ isNew ? '创建新演讲' : '编辑演讲' }}</h2>
      </div>

      <form class="edit-form" @submit.prevent="handleSubmit">
        <div class="form-section">
          <div class="form-group">
            <label>演讲标题</label>
            <input 
              type="text" 
              v-model="formData.title"
              placeholder="请输入演讲标题"
              required
            />
          </div>

          <div class="form-group">
            <label>演讲描述</label>
            <textarea 
              v-model="formData.description"
              placeholder="请输入演讲描述"
              rows="4"
              required
            ></textarea>
          </div>

          <div class="form-group">
            <label>演讲时间</label>
            <div class="datetime-inputs">
              <input 
                type="date" 
                v-model="formData.date"
                required
              />
              <input 
                type="time" 
                v-model="formData.time"
                required
              />
            </div>
          </div>

          <div class="form-group">
            <label>预计时长（分钟）</label>
            <input 
              type="number" 
              v-model="formData.duration"
              min="1"
              required
            />
          </div>

          <div class="form-group">
            <label>最大参与人数</label>
            <input 
              type="number" 
              v-model="formData.maxParticipants"
              min="1"
              required
            />
          </div>

          <div class="form-group">
            <label>演讲地点/链接</label>
            <input 
              type="text" 
              v-model="formData.location"
              placeholder="线下地点或在线会议链接"
              required
            />
          </div>
        </div>

        <div class="divider"></div>

        <div class="form-section">
          <h3>演讲设置</h3>
          
          <div class="settings-grid">
            <div class="setting-item">
              <label class="toggle-label">
                <span>允许提前加入</span>
                <div class="toggle-switch">
                  <input 
                    type="checkbox"
                    v-model="formData.settings.allowEarlyJoin"
                  />
                  <span class="slider"></span>
                </div>
              </label>
            </div>

            <div class="setting-item">
              <label class="toggle-label">
                <span>开启实时反馈</span>
                <div class="toggle-switch">
                  <input 
                    type="checkbox"
                    v-model="formData.settings.enableFeedback"
                  />
                  <span class="slider"></span>
                </div>
              </label>
            </div>

            <div class="setting-item">
              <label class="toggle-label">
                <span>允许题目讨论</span>
                <div class="toggle-switch">
                  <input 
                    type="checkbox"
                    v-model="formData.settings.enableDiscussion"
                  />
                  <span class="slider"></span>
                </div>
              </label>
            </div>

            <div class="setting-item">
              <label class="toggle-label">
                <span>自动录制</span>
                <div class="toggle-switch">
                  <input 
                    type="checkbox"
                    v-model="formData.settings.autoRecord"
                  />
                  <span class="slider"></span>
                </div>
              </label>
            </div>
          </div>
        </div>

        <div class="action-section">
          <button 
            type="button" 
            class="action-button secondary"
            @click="goBack"
          >
            取消
          </button>
          <button 
            type="submit" 
            class="action-button"
          >
            {{ isNew ? '创建' : '保存' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';

const props = defineProps({
  presentationId: {
    type: String,
    default: ''
  }
});

const router = useRouter();
const isNew = computed(() => !props.presentationId);

const formData = ref({
  title: '',
  description: '',
  date: '',
  time: '',
  duration: 60,
  maxParticipants: 30,
  location: '',
  settings: {
    allowEarlyJoin: true,
    enableFeedback: true,
    enableDiscussion: true,
    autoRecord: false
  }
});

const handleSubmit = () => {
  // TODO: 实现提交逻辑
  console.log('提交表单:', formData.value);
};

const goBack = () => {
  router.back();
};
</script>

<style scoped>
.presentation-edit {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.header-section h2 {
  color: #4dc189;
  margin-bottom: 20px;
}

.edit-form {
  display: flex;
  flex-direction: column;
  gap: 30px;
}

.form-section {
  background-color: #f9f9f9;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

h3 {
  color: #333;
  margin-bottom: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 20px;
}

.form-group:last-child {
  margin-bottom: 0;
}

label {
  color: #333;
  font-weight: bold;
  font-size: 14px;
}

input[type="text"],
input[type="number"],
input[type="date"],
input[type="time"],
textarea {
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
  color: #333;
  transition: all 0.3s ease;
}

input:focus,
textarea:focus {
  outline: none;
  border-color: #4dc189;
  box-shadow: 0 0 0 2px rgba(77, 193, 137, 0.1);
}

.datetime-inputs {
  display: flex;
  gap: 10px;
}

.datetime-inputs input {
  flex: 1;
}

.divider {
  height: 1px;
  background-color: #eee;
  margin: 20px 0;
}

.settings-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
}

.setting-item {
  background-color: #fff;
  border-radius: 6px;
  padding: 15px;
}

.toggle-label {
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
}

.toggle-switch {
  position: relative;
  display: inline-block;
  width: 40px;
  height: 20px;
}

.toggle-switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

.slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #ccc;
  transition: .4s;
  border-radius: 20px;
}

.slider:before {
  position: absolute;
  content: "";
  height: 16px;
  width: 16px;
  left: 2px;
  bottom: 2px;
  background-color: white;
  transition: .4s;
  border-radius: 50%;
}

input:checked + .slider {
  background-color: #4dc189;
}

input:checked + .slider:before {
  transform: translateX(20px);
}

.action-section {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 20px;
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

.action-button.secondary {
  background-color: #fff;
  color: #4dc189;
}

.action-button.secondary:hover {
  background-color: #f0f9f4;
}
</style>
