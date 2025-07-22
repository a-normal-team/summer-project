/**
 * 讨论区服务
 * 提供与讨论区相关的API请求功能
 */

import { get, post } from './http';

/**
 * 获取题目的所有评论
 * @param {number} questionId - 题目ID
 * @returns {Promise} - 包含评论列表的Promise
 */
export async function getComments(questionId) {
  try {
    const data = await get(`/discussion/questions/${questionId}/comments`);
    return data;
  } catch (error) {
    console.error(`获取题目(ID: ${questionId})评论失败:`, error);
    throw error;
  }
}

/**
 * 添加新评论
 * @param {number} questionId - 题目ID
 * @param {Object} commentData - 评论数据
 * @param {string} commentData.commentText - 评论内容
 * @param {number} [commentData.parentCommentId] - 父评论ID (回复评论时使用)
 * @returns {Promise} - 包含添加结果的Promise
 */
export async function addComment(questionId, commentData) {
  try {
    const data = await post(`/discussion/questions/${questionId}/comments`, {
      comment_text: commentData.commentText,
      parent_comment_id: commentData.parentCommentId
    });
    return data;
  } catch (error) {
    console.error(`添加评论失败:`, error);
    throw error;
  }
}
