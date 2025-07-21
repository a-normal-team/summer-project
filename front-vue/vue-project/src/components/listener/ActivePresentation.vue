<template>
  <div class="active-presentation">
    <h2>当前演讲</h2>
    <div class="active-question">
      <p>当前题目: Flask 是一个什么类型的框架？</p>
      <div class="options">
        <button class="option-button">微框架</button>
        <button class="option-button">全栈框架</button>
        <button class="option-button">前端框架</button>
        <button class="option-button">数据库框架</button>
      </div>
      <button class="submit-answer-button">提交答案</button>
    </div>
    <div class="feedback-section">
      <h3>即时反馈</h3>
      <div class="feedback-buttons">
        <button class="feedback-button">讲得太快</button>
        <button class="feedback-button">讲得太慢</button>
        <button class="feedback-button">内容乏味</button>
        <button class="feedback-button">题目质量差</button>
      </div>
    </div>
  </div>
</template>

<script setup>
// 当前演讲逻辑
</script>

<style scoped>
.active-presentation {
  padding: 20px;
}
</style>
