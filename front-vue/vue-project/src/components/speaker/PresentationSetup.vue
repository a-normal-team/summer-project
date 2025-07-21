<template>
  <div class="sub-dashboard-section">
    <div class="presentation-setup">
      <h2>演讲设置</h2>
      
      <div class="setup-section">
        <div class="file-upload-card">
          <h3>演讲材料</h3>
          <div class="upload-area" @drop.prevent="handleDrop" @dragover.prevent>
            <div class="upload-content">
              <span class="upload-icon">📄</span>
              <p>将文件拖放到此处，或</p>
              <button class="action-button" @click="triggerFileInput">
                选择文件
              </button>
              <input
                type="file"
                ref="fileInput"
                style="display: none"
                @change="handleFileSelect"
                accept=".pdf,.pptx,.doc,.docx,.txt"
              />
            </div>
          </div>
          
          <div v-if="uploadedFiles.length > 0" class="uploaded-files">
            <h4>已上传文件</h4>
            <div class="file-list">
              <div v-for="file in uploadedFiles" :key="file.id" class="file-item">
                <div class="file-info">
                  <span class="file-icon">{{ getFileIcon(file.type) }}</span>
                  <span class="file-name">{{ file.name }}</span>
                  <span class="file-size">{{ formatFileSize(file.size) }}</span>
                </div>
                <div class="file-actions">
                  <button class="action-button small" @click="previewFile(file)">
                    预览
                  </button>
                  <button class="action-button small danger" @click="removeFile(file)">
                    删除
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="settings-card">
          <h3>演讲设置</h3>
          <div class="settings-form">
            <div class="form-group">
              <label>演讲时长（分钟）</label>
              <input type="number" v-model="settings.duration" min="1" />
            </div>
            
            <div class="form-group">
              <label>题目数量</label>
              <input type="number" v-model="settings.quizCount" min="1" />
            </div>
            
            <div class="form-group">
              <label>每题作答时间（秒）</label>
              <input type="number" v-model="settings.quizDuration" min="10" />
            </div>
            
            <div class="form-group">
              <label>是否自动生成题目</label>
              <div class="toggle-switch">
                <input
                  type="checkbox"
                  id="autoGenerate"
                  v-model="settings.autoGenerate"
                />
                <label for="autoGenerate"></label>
              </div>
            </div>
            
            <div class="form-group">
              <label>是否允许讨论</label>
              <div class="toggle-switch">
                <input
                  type="checkbox"
                  id="allowDiscussion"
                  v-model="settings.allowDiscussion"
                />
                <label for="allowDiscussion"></label>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="action-section">
        <button class="action-button secondary" @click="saveAsDraft">
          保存草稿
        </button>
        <button class="action-button" @click="saveAndPublish">
          保存并发布
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const fileInput = ref(null);
const uploadedFiles = ref([]);
const settings = ref({
  duration: 60,
  quizCount: 5,
  quizDuration: 30,
  autoGenerate: true,
  allowDiscussion: true
});

const triggerFileInput = () => {
  fileInput.value.click();
};

const handleFileSelect = (event) => {
  const files = Array.from(event.target.files);
  processFiles(files);
};

const handleDrop = (event) => {
  const files = Array.from(event.dataTransfer.files);
  processFiles(files);
};

const processFiles = (files) => {
  files.forEach(file => {
    uploadedFiles.value.push({
      id: Date.now(),
      name: file.name,
      size: file.size,
      type: file.type,
      file: file
    });
  });
};

const removeFile = (file) => {
  const index = uploadedFiles.value.findIndex(f => f.id === file.id);
  if (index !== -1) {
    uploadedFiles.value.splice(index, 1);
  }
};

const getFileIcon = (type) => {
  const icons = {
    'application/pdf': '📄',
    'application/vnd.openxmlformats-officedocument.presentationml.presentation': '📊',
    'application/msword': '📝',
    'text/plain': '📃'
  };
  return icons[type] || '📎';
};

const formatFileSize = (size) => {
  const units = ['B', 'KB', 'MB', 'GB'];
  let i = 0;
  while (size >= 1024 && i < units.length - 1) {
    size /= 1024;
    i++;
  }
  return `${size.toFixed(1)} ${units[i]}`;
};

const previewFile = (file) => {
  // TODO: 实现文件预览逻辑
  console.log('预览文件:', file);
};

const saveAsDraft = () => {
  // TODO: 实现保存草稿逻辑
  console.log('保存草稿:', { settings: settings.value, files: uploadedFiles.value });
};

const saveAndPublish = () => {
  // TODO: 实现保存并发布逻辑
  console.log('保存并发布:', { settings: settings.value, files: uploadedFiles.value });
};
</script>

<style scoped>
.presentation-setup {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

h2 {
  color: #4dc189;
  margin-bottom: 20px;
}

.setup-section {
  display: grid;
  gap: 20px;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
}

.file-upload-card,
.settings-card {
  background-color: #f9f9f9;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

h3 {
  color: #333;
  margin-bottom: 20px;
}

.upload-area {
  border: 2px dashed #ddd;
  border-radius: 8px;
  padding: 30px;
  text-align: center;
  background-color: #fff;
  transition: all 0.3s ease;
  cursor: pointer;
}

.upload-area:hover {
  border-color: #4dc189;
  background-color: #f0f9f4;
}

.upload-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
}

.upload-icon {
  font-size: 40px;
  margin-bottom: 10px;
}

.uploaded-files {
  margin-top: 20px;
}

.uploaded-files h4 {
  color: #666;
  margin-bottom: 10px;
}

.file-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.file-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px;
  background-color: #fff;
  border-radius: 6px;
  border: 1px solid #eee;
}

.file-info {
  display: flex;
  align-items: center;
  gap: 10px;
}

.file-icon {
  font-size: 20px;
}

.file-name {
  color: #333;
  font-size: 14px;
}

.file-size {
  color: #666;
  font-size: 12px;
}

.file-actions {
  display: flex;
  gap: 10px;
}

.settings-form {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.form-group {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.form-group label {
  color: #333;
  font-size: 14px;
}

.form-group input[type="number"] {
  width: 100px;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

/* 开关样式 */
.toggle-switch {
  position: relative;
  width: 50px;
  height: 24px;
}

.toggle-switch input {
  display: none;
}

.toggle-switch label {
  position: absolute;
  top: 0;
  left: 0;
  width: 50px;
  height: 24px;
  background-color: #ddd;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.toggle-switch label::after {
  content: '';
  position: absolute;
  top: 2px;
  left: 2px;
  width: 20px;
  height: 20px;
  background-color: #fff;
  border-radius: 50%;
  transition: all 0.3s ease;
}

.toggle-switch input:checked + label {
  background-color: #4dc189;
}

.toggle-switch input:checked + label::after {
  transform: translateX(26px);
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

.action-button.small {
  padding: 4px 8px;
  font-size: 12px;
}

.action-button.secondary {
  background-color: #fff;
  color: #4dc189;
}

.action-button.secondary:hover {
  background-color: #f0f9f4;
}

.action-button.danger {
  background-color: #dc3545;
  border-color: #dc3545;
}

.action-button.danger:hover {
  background-color: #bb2d3b;
  border-color: #bb2d3b;
}
</style>
