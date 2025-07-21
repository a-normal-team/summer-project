<template>
  <div class="sub-dashboard-section">
    <div class="quiz-discussion">
      <div class="quiz-content">
        <h2>题目讨论</h2>
        <div class="quiz-card">
          <div class="quiz-header">
            <span class="quiz-number">题目 #{{ quizNumber }}</span>
            <span class="quiz-status" :class="{ 'correct': isCorrect }">
              {{ isCorrect ? '回答正确' : '回答错误' }}
            </span>
          </div>
          <p class="question">{{ quiz.question }}</p>
          <div class="options-list">
            <div 
              v-for="option in quiz.options" 
              :key="option.id"
              class="option-item"
              :class="{
                'correct': option.id === quiz.correctAnswer,
                'selected': option.id === selectedAnswer
              }"
            >
              {{ option.text }}
            </div>
          </div>
          <div class="explanation" v-if="quiz.explanation">
            <h3>解释</h3>
            <p>{{ quiz.explanation }}</p>
          </div>
        </div>
      </div>

      <div class="discussion-section">
        <DiscussionArea
          :comments="comments"
          :current-user="currentUser"
          :is-logged-in="true"
          @submit="submitComment"
          @reply="replyToComment"
          @delete="deleteComment"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineProps, ref } from 'vue';
import DiscussionArea from '../common/DiscussionArea.vue';

const props = defineProps({
  quizId: {
    type: String,
    required: true
  },
  quizNumber: {
    type: Number,
    required: true
  },
  quiz: {
    type: Object,
    required: true
  },
  currentUser: {
    type: Object,
    required: true
  }
});

const comments = ref([]);
const selectedAnswer = ref(null);
const isCorrect = ref(false);

// 提交评论
const submitComment = (comment) => {
  // TODO: 实现评论提交逻辑
  console.log('提交评论:', comment);
};

// 回复评论
const replyToComment = (comment) => {
  // TODO: 实现回复评论逻辑
  console.log('回复评论:', comment);
};

// 删除评论
const deleteComment = (commentId) => {
  // TODO: 实现删除评论逻辑
  console.log('删除评论:', commentId);
};
</script>

<style scoped>
.quiz-discussion {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

h2 {
  color: #4dc189;
  margin-bottom: 20px;
}

.quiz-card {
  background-color: #f9f9f9;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.quiz-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.quiz-number {
  font-weight: bold;
  color: #333;
}

.quiz-status {
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: bold;
  background-color: #dc3545;
  color: white;
}

.quiz-status.correct {
  background-color: #28a745;
}

.question {
  font-size: 16px;
  color: #333;
  margin-bottom: 15px;
  line-height: 1.5;
}

.options-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-bottom: 20px;
}

.option-item {
  padding: 10px 15px;
  border-radius: 6px;
  background-color: #fff;
  border: 1px solid #ddd;
  color: #333;
}

.option-item.selected {
  border-color: #4dc189;
  background-color: #f0f9f4;
}

.option-item.correct {
  border-color: #28a745;
  background-color: #d4edda;
  color: #155724;
}

.option-item.selected:not(.correct) {
  border-color: #dc3545;
  background-color: #f8d7da;
  color: #721c24;
}

.explanation {
  background-color: #fff;
  border-radius: 6px;
  padding: 15px;
  margin-top: 15px;
}

.explanation h3 {
  color: #4dc189;
  margin-bottom: 10px;
  font-size: 16px;
}

.explanation p {
  color: #666;
  line-height: 1.5;
  font-size: 14px;
}

.discussion-section {
  margin-top: 20px;
}
</style>
