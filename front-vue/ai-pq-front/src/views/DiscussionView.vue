<template>
  <div class="discussion-container">
    <h2>题目讨论区</h2>
    <div class="question-info">
      <h3>题目: {{ question.text }}</h3>
    </div>

    <div class="comments-section">
      <h3>评论</h3>
      <div v-if="comments.length === 0" class="no-comments">
        <p>暂无评论，快来发表你的看法吧！</p>
      </div>
      <div v-else class="comment-list">
        <div v-for="comment in comments" :key="comment.id" class="comment-item">
          <p class="comment-author">{{ comment.author }} <span class="comment-date">{{ comment.date }}</span></p>
          <p class="comment-content">{{ comment.content }}</p>
          <button @click="replyToComment(comment.id)">回复</button>
          <div v-if="comment.replies && comment.replies.length > 0" class="replies">
            <div v-for="reply in comment.replies" :key="reply.id" class="comment-item reply-item">
              <p class="comment-author">{{ reply.author }} <span class="comment-date">{{ reply.date }}</span></p>
              <p class="comment-content">{{ reply.content }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="comment-form">
      <h3>发表评论</h3>
      <textarea v-model="newCommentContent" placeholder="输入你的评论..." rows="4"></textarea>
      <button @click="submitComment" :disabled="!newCommentContent.trim()">提交评论</button>
    </div>

    <button @click="router.back()">返回</button>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';

const route = useRoute();
const router = useRouter();

interface DiscussionQuestion {
  id: number | null;
  text: string;
}

const question = ref<DiscussionQuestion>({
  id: null,
  text: '加载中...',
});

const comments = ref([
  // 模拟评论数据
  { id: 1, author: '用户A', date: '2023-07-19 10:00', content: '我觉得这道题的选项C有点歧义。', replies: [] },
  { id: 2, author: '用户B', date: '2023-07-19 10:15', content: '同意楼上，我当时也犹豫了。', replies: [
    { id: 2.1, author: '用户C', date: '2023-07-19 10:30', content: '确实，如果能更明确就好了。' }
  ] },
]);

const newCommentContent = ref('');

onMounted(() => {
  if (route.params.id) {
    question.value.id = Number(route.params.id);
    // 实际应用中，这里会调用API获取题目详情和评论
    console.log(`加载讨论区数据: ${question.value.id}`);
    // 模拟加载数据
    question.value.text = '以下哪个不是Spring Boot的特点？';
  }
});

const submitComment = () => {
  if (newCommentContent.value.trim()) {
    const newComment = {
      id: Date.now(), // 简单生成ID
      author: '当前用户', // 实际应从认证信息获取
      date: new Date().toLocaleString(),
      content: newCommentContent.value.trim(),
      replies: [],
    };
    comments.value.push(newComment);
    alert('评论已提交！');
    newCommentContent.value = '';
    // 调用提交评论API
  }
};

const replyToComment = (commentId: number) => {
  const replyContent = prompt('输入你的回复:');
  if (replyContent && replyContent.trim()) {
    const parentComment = comments.value.find(c => c.id === commentId);
    if (parentComment) {
      if (!parentComment.replies) {
        parentComment.replies = [];
      }
      parentComment.replies.push({
        id: Date.now() + 0.1, // 简单生成回复ID
        author: '当前用户',
        date: new Date().toLocaleString(),
        content: replyContent.trim(),
      });
      alert('回复已提交！');
      // 调用提交回复API
    }
  }
};
</script>

<style scoped>
.discussion-container {
  max-width: 800px;
  margin: 50px auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  text-align: left;
}

h2 {
  color: #333;
  margin-bottom: 20px;
  text-align: center;
}

.question-info {
  background-color: #e7f3ff;
  border: 1px solid #b3d9ff;
  padding: 15px;
  border-radius: 6px;
  margin-bottom: 30px;
  text-align: center;
}

.question-info h3 {
  margin: 0;
  color: #007bff;
}

.comments-section {
  margin-bottom: 30px;
}

.comments-section h3 {
  color: #555;
  margin-bottom: 15px;
  border-bottom: 1px solid #ddd;
  padding-bottom: 10px;
}

.no-comments {
  color: #999;
  font-style: italic;
  text-align: center;
  padding: 20px;
}

.comment-list {
  border: 1px solid #eee;
  border-radius: 6px;
  padding: 15px;
  background-color: #f9f9f9;
}

.comment-item {
  margin-bottom: 15px;
  padding-bottom: 15px;
  border-bottom: 1px dashed #ddd;
}

.comment-item:last-child {
  border-bottom: none;
  margin-bottom: 0;
  padding-bottom: 0;
}

.comment-author {
  font-weight: bold;
  color: #333;
  margin-bottom: 5px;
}

.comment-date {
  font-weight: normal;
  color: #999;
  font-size: 0.9em;
  margin-left: 10px;
}

.comment-content {
  color: #444;
  line-height: 1.6;
  margin-bottom: 10px;
}

.comment-item button {
  background-color: #17a2b8;
  color: white;
  padding: 5px 10px;
  border: none;
  border-radius: 3px;
  cursor: pointer;
  font-size: 0.9em;
}

.comment-item button:hover {
  background-color: #138496;
}

.replies {
  margin-top: 10px;
  padding-left: 20px;
  border-left: 2px solid #eee;
}

.reply-item {
  background-color: #ffffff;
  padding: 10px;
  margin-top: 10px;
  border: 1px solid #f0f0f0;
  border-radius: 4px;
}

.comment-form {
  background-color: #f9f9f9;
  border: 1px solid #eee;
  border-radius: 6px;
  padding: 15px;
}

.comment-form h3 {
  color: #555;
  margin-top: 0;
  margin-bottom: 15px;
  border-bottom: 1px solid #ddd;
  padding-bottom: 10px;
}

.comment-form textarea {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  box-sizing: border-box;
  margin-bottom: 15px;
  resize: vertical;
}

.comment-form button {
  background-color: #007bff;
  color: white;
  padding: 10px 15px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
}

.comment-form button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

.comment-form button:hover:not(:disabled) {
  background-color: #0056b3;
}

.discussion-container > button {
  display: block;
  width: 150px;
  margin: 30px auto 0;
  background-color: #6c757d;
  color: white;
  padding: 10px 15px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
}

.discussion-container > button:hover {
  background-color: #5a6268;
}
</style>
