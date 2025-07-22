/**
 * 测验服务
 * 提供与测验相关的API请求功能
 */

import { get, post } from './http';

/**
 * 为演讲创建新题目
 * @param {number} presentationId - 演讲ID
 * @param {Object} questionData - 题目数据
 * @returns {Promise} - 包含创建结果的Promise
 */
export async function createQuestion(presentationId, questionData) {
  try {
    const data = await post(`/quiz/presentations/${presentationId}/questions`, questionData);
    return data;
  } catch (error) {
    console.error('创建题目失败:', error);
    throw error;
  }
}

/**
 * 获取演讲当前活跃的题目
 * @param {number} presentationId - 演讲ID
 * @returns {Promise} - 包含活跃题目的Promise
 */
export async function getActiveQuestion(presentationId) {
  try {
    const data = await get(`/quiz/presentations/${presentationId}/active_question`);
    return data;
  } catch (error) {
    console.error(`获取演讲(ID: ${presentationId})活跃题目失败:`, error);
    throw error;
  }
}

/**
 * 提交题目答案
 * @param {number} questionId - 题目ID
 * @param {number} selectedOptionIndex - 选择的答案选项索引
 * @returns {Promise} - 包含提交结果的Promise
 */
export async function submitAnswer(questionId, selectedOptionIndex) {
  try {
    // 获取当前用户ID (实际项目中应该从全局状态或服务中获取)
    const userId = 1; // 模拟当前用户ID
    
    const data = await post(`/quiz/questions/${questionId}/answer`, {
      user_id: userId,
      answer: selectedOptionIndex // 发送所选选项的索引
    });
    return data;
  } catch (error) {
    console.error(`提交答案失败:`, error);
    throw error;
  }
}

/**
 * 停用题目
 * @param {number} questionId - 题目ID
 * @returns {Promise} - 包含操作结果的Promise
 */
export async function deactivateQuestion(questionId) {
  try {
    const data = await post(`/quiz/questions/${questionId}/deactivate`, {});
    return data;
  } catch (error) {
    console.error(`停用题目失败:`, error);
    throw error;
  }
}

/**
 * 获取题目统计
 * @param {number} questionId - 题目ID
 * @returns {Promise} - 包含题目统计的Promise
 */
export async function getQuestionStats(questionId) {
  try {
    const data = await get(`/quiz/questions/${questionId}/stats`);
    return data;
  } catch (error) {
    console.error(`获取题目统计失败:`, error);
    throw error;
  }
}

/**
 * 获取听众个人报告
 * @param {number} presentationId - 演讲ID
 * @param {number} userId - 用户ID
 * @returns {Promise} - 包含个人报告的Promise
 */
export async function getUserReport(presentationId, userId) {
  try {
    const data = await get(`/quiz/presentations/${presentationId}/report/${userId}`);
    return data;
  } catch (error) {
    console.error(`获取个人报告失败:`, error);
    throw error;
  }
}

/**
 * 获取演讲整体统计
 * @param {number} presentationId - 演讲ID
 * @returns {Promise} - 包含演讲统计的Promise
 */
export async function getPresentationStats(presentationId) {
  try {
    const data = await get(`/quiz/presentations/${presentationId}/overall_stats`);
    return data;
  } catch (error) {
    console.error(`获取演讲统计失败:`, error);
    throw error;
  }
}

/**
 * 从文件生成题目
 * @param {number} fileId - 文件ID
 * @param {number} presentationId - 演讲ID
 * @returns {Promise} - 包含生成结果的Promise
 */
export async function generateQuestionsFromFile(fileId, presentationId) {
  try {
    const data = await post(`/quiz/generate_questions`, { file_id: fileId, presentation_id: presentationId });
    return data;
  } catch (error) {
    console.error(`从文件生成题目失败:`, error);
    throw error;
  }
}

/**
 * 获取演讲的所有题目
 * @param {number} presentationId - 演讲ID
 * @returns {Promise} - 包含题目列表的Promise
 */
export async function getPresentationQuestions(presentationId) {
  try {
    const data = await get(`/quiz/presentations/${presentationId}/questions`);
    return data;
  } catch (error) {
    console.error(`获取演讲题目列表失败:`, error);
    throw error;
  }
}

/**
 * 题目服务默认导出
 */
export default {
  createQuestion,
  getActiveQuestion,
  submitAnswer,
  deactivateQuestion,
  getQuestionStats,
  getUserReport,
  getPresentationStats,
  generateQuestionsFromFile,
  getPresentationQuestions
};
