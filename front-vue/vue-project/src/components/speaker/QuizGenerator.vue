<template>
  <div class="sub-dashboard-section">
    <div class="quiz-generator">
      <div class="header-section">
        <h2>题目生成</h2>
        <div class="mode-switch">
          <button 
            v-for="mode in generationModes" 
            :key="mode.value"
            class="mode-button"
            :class="{ active: selectedMode === mode.value }"
            @click="selectedMode = mode.value"
          >
            {{ mode.label }}
          </button>
        </div>
      </div>

      <div class="generator-content">
        <div class="settings-card" v-if="selectedMode === 'auto'">
          <h3>自动生成设置</h3>
          <div class="settings-form">
            <div class="form-group">
              <label>选择章节</label>
              <div class="chapter-select">
                <div 
                  v-for="chapter in chapters" 
                  :key="chapter.id"
                  class="chapter-item"
                  :class="{ selected: selectedChapters.includes(chapter.id) }"
                  @click="toggleChapter(chapter.id)"
                >
                  <span class="chapter-name">{{ chapter.name }}</span>
                  <span class="page-range">P{{ chapter.startPage }}-{{ chapter.endPage }}</span>
                </div>
              </div>
            </div>

            <div class="form-group">
              <label>题目数量</label>
              <div class="number-input">
                <button @click="decreaseCount">-</button>
                <input type="number" v-model="quizCount" min="1" max="10" />
                <button @click="increaseCount">+</button>
              </div>
            </div>

            <div class="form-group">
              <label>难度级别</label>
              <div class="difficulty-select">
                <button 
                  v-for="level in difficultyLevels" 
                  :key="level.value"
                  class="difficulty-button"
                  :class="{ active: selectedDifficulty === level.value }"
                  @click="selectedDifficulty = level.value"
                >
                  {{ level.label }}
                </button>
              </div>
            </div>
          </div>
        </div>

        <div class="editor-card" v-else>
          <h3>手动编辑</h3>
          <div class="quiz-editor">
            <div class="form-group">
              <label>题目描述</label>
              <textarea 
                v-model="manualQuiz.question"
                placeholder="请输入题目描述..."
                rows="3"
              ></textarea>
            </div>

            <div class="form-group">
              <label>选项</label>
              <div class="options-list">
                <div 
                  v-for="(option, index) in manualQuiz.options" 
                  :key="index"
                  class="option-input"
                >
                  <input 
                    type="text" 
                    v-model="option.text"
                    :placeholder="`选项 ${index + 1}`"
                  />
                  <input 
                    type="radio" 
                    :name="'correct'" 
                    :value="option.id"
                    v-model="manualQuiz.correctAnswer"
                  />
                  <button class="remove-option" @click="removeOption(index)">×</button>
                </div>
              </div>
              <button class="add-option" @click="addOption">
                添加选项
              </button>
            </div>

            <div class="form-group">
              <label>解释</label>
              <textarea 
                v-model="manualQuiz.explanation"
                placeholder="请输入答案解释..."
                rows="2"
              ></textarea>
            </div>
          </div>
        </div>

        <div class="preview-card" v-if="previewQuiz">
          <h3>预览</h3>
          <div class="quiz-preview">
            <p class="question">{{ previewQuiz.question }}</p>
            <div class="options-preview">
              <div 
                v-for="option in previewQuiz.options" 
                :key="option.id"
                class="option-item"
                :class="{ correct: option.id === previewQuiz.correctAnswer }"
              >
                {{ option.text }}
              </div>
            </div>
            <div class="explanation" v-if="previewQuiz.explanation">
              <h4>解释</h4>
              <p>{{ previewQuiz.explanation }}</p>
            </div>
          </div>
        </div>
      </div>

      <div class="action-section">
        <button 
          v-if="selectedMode === 'auto'"
          class="action-button generate"
          @click="generateQuiz"
          :disabled="!canGenerate"
        >
          生成题目
        </button>
        <button 
          v-else
          class="action-button"
          @click="saveQuiz"
          :disabled="!canSave"
        >
          保存题目
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';

const generationModes = [
  { label: '自动生成', value: 'auto' },
  { label: '手动编辑', value: 'manual' }
];

const difficultyLevels = [
  { label: '简单', value: 'easy' },
  { label: '中等', value: 'medium' },
  { label: '困难', value: 'hard' }
];

const chapters = [
  { id: 1, name: '第一章：介绍', startPage: 1, endPage: 10 },
  { id: 2, name: '第二章：基础概念', startPage: 11, endPage: 25 },
  { id: 3, name: '第三章：高级特性', startPage: 26, endPage: 40 }
];

const selectedMode = ref('auto');
const selectedChapters = ref([]);
const quizCount = ref(1);
const selectedDifficulty = ref('medium');

const manualQuiz = ref({
  question: '',
  options: [
    { id: 'A', text: '' },
    { id: 'B', text: '' },
    { id: 'C', text: '' },
    { id: 'D', text: '' }
  ],
  correctAnswer: '',
  explanation: ''
});

const previewQuiz = ref(null);

const canGenerate = computed(() => {
  return selectedChapters.value.length > 0 && quizCount.value > 0;
});

const canSave = computed(() => {
  return manualQuiz.value.question &&
         manualQuiz.value.options.every(o => o.text) &&
         manualQuiz.value.correctAnswer;
});

const toggleChapter = (chapterId) => {
  const index = selectedChapters.value.indexOf(chapterId);
  if (index === -1) {
    selectedChapters.value.push(chapterId);
  } else {
    selectedChapters.value.splice(index, 1);
  }
};

const decreaseCount = () => {
  if (quizCount.value > 1) quizCount.value--;
};

const increaseCount = () => {
  if (quizCount.value < 10) quizCount.value++;
};

const addOption = () => {
  if (manualQuiz.value.options.length < 6) {
    const nextId = String.fromCharCode(65 + manualQuiz.value.options.length);
    manualQuiz.value.options.push({ id: nextId, text: '' });
  }
};

const removeOption = (index) => {
  if (manualQuiz.value.options.length > 2) {
    manualQuiz.value.options.splice(index, 1);
    if (manualQuiz.value.correctAnswer === manualQuiz.value.options[index]?.id) {
      manualQuiz.value.correctAnswer = '';
    }
  }
};

const generateQuiz = () => {
  // TODO: 实现自动生成题目的逻辑
  console.log('生成题目:', {
    chapters: selectedChapters.value,
    count: quizCount.value,
    difficulty: selectedDifficulty.value
  });
};

const saveQuiz = () => {
  // TODO: 实现保存手动编辑题目的逻辑
  console.log('保存题目:', manualQuiz.value);
};
</script>

<style scoped>
.quiz-generator {
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

.mode-switch {
  display: flex;
  gap: 10px;
}

.mode-button {
  padding: 8px 16px;
  border-radius: 20px;
  border: 1px solid #ddd;
  background-color: #fff;
  color: #666;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.mode-button:hover {
  border-color: #4dc189;
  color: #4dc189;
}

.mode-button.active {
  background-color: #4dc189;
  border-color: #4dc189;
  color: #fff;
}

.generator-content {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.settings-card,
.editor-card,
.preview-card {
  background-color: #f9f9f9;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

h3 {
  color: #333;
  margin-bottom: 20px;
}

.settings-form,
.quiz-editor {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.form-group label {
  color: #333;
  font-weight: bold;
}

.chapter-select {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 10px;
}

.chapter-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px;
  background-color: #fff;
  border: 1px solid #ddd;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.chapter-item:hover {
  border-color: #4dc189;
}

.chapter-item.selected {
  background-color: #4dc189;
  border-color: #4dc189;
  color: white;
}

.chapter-name {
  font-size: 14px;
}

.page-range {
  font-size: 12px;
  color: #666;
}

.chapter-item.selected .page-range {
  color: #fff;
}

.number-input {
  display: flex;
  align-items: center;
  gap: 10px;
  width: fit-content;
}

.number-input button {
  width: 30px;
  height: 30px;
  border-radius: 15px;
  border: 1px solid #ddd;
  background-color: #fff;
  color: #333;
  cursor: pointer;
}

.number-input input {
  width: 50px;
  text-align: center;
  border: 1px solid #ddd;
  border-radius: 4px;
  padding: 5px;
}

.difficulty-select {
  display: flex;
  gap: 10px;
}

.difficulty-button {
  flex: 1;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
  background-color: #fff;
  color: #666;
  cursor: pointer;
  transition: all 0.3s ease;
}

.difficulty-button:hover {
  border-color: #4dc189;
  color: #4dc189;
}

.difficulty-button.active {
  background-color: #4dc189;
  border-color: #4dc189;
  color: #fff;
}

textarea {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  resize: vertical;
}

.options-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.option-input {
  display: flex;
  align-items: center;
  gap: 10px;
}

.option-input input[type="text"] {
  flex-grow: 1;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.remove-option {
  width: 24px;
  height: 24px;
  border-radius: 12px;
  border: none;
  background-color: #dc3545;
  color: white;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
}

.add-option {
  padding: 8px;
  border: 1px dashed #4dc189;
  border-radius: 4px;
  background-color: transparent;
  color: #4dc189;
  cursor: pointer;
  margin-top: 10px;
}

.quiz-preview {
  background-color: #fff;
  border-radius: 6px;
  padding: 20px;
}

.question {
  color: #333;
  font-size: 16px;
  margin-bottom: 20px;
  line-height: 1.5;
}

.options-preview {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.option-item {
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  background-color: #f9f9f9;
}

.option-item.correct {
  border-color: #28a745;
  background-color: #d4edda;
  color: #155724;
}

.explanation {
  margin-top: 20px;
  padding-top: 20px;
  border-top: 1px solid #eee;
}

.explanation h4 {
  color: #4dc189;
  margin-bottom: 10px;
}

.action-section {
  display: flex;
  justify-content: flex-end;
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

.action-button:hover:not(:disabled) {
  background-color: #3aa875;
  transform: translateY(-1px);
}

.action-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.action-button.generate {
  background-color: #28a745;
  border-color: #28a745;
}

.action-button.generate:hover:not(:disabled) {
  background-color: #218838;
  border-color: #1e7e34;
}
</style>
