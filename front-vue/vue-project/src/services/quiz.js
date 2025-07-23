/**
 * 测验服务
 * 提供与测验相关的API请求功能
 */

import { get, post } from './http';
import { API_CONFIG, AUTH_CONFIG } from '../config';

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
 * 获取演讲当前所有活跃的题目
 * @param {number} presentationId - 演讲ID
 * @returns {Promise} - 包含所有活跃题目的Promise
 */
export async function getActiveQuestions(presentationId) {
  try {
    const data = await get(`/quiz/presentations/${presentationId}/active_questions`);
    console.log('活跃题目API返回数据:', data); // 添加日志，便于调试
    
    // 根据API返回格式灵活处理
    if (Array.isArray(data)) {
      return data; // 如果直接返回数组，就使用这个数组
    } else if (data && data.active_questions) {
      return data.active_questions; // 如果返回对象包含active_questions字段，则使用该字段
    } else {
      return []; // 其他情况返回空数组
    }
  } catch (error) {
    console.error(`获取演讲(ID: ${presentationId})所有活跃题目失败:`, error);
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
    // 将选项索引转换为对应的字母答案（A、B、C、D...）
    const answerText = String.fromCharCode(65 + selectedOptionIndex);
    
    // 确保URL路径正确，使用/api/quiz/questions/...格式
    const endpoint = `/api/quiz/questions/${questionId}/answer`;
    console.log(`提交答案到 ${endpoint}`, { answer_text: answerText });
    
    // 使用带完整路径的请求
    const response = await fetch(`${API_CONFIG.BASE_URL.replace('/api', '')}${endpoint}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': localStorage.getItem(AUTH_CONFIG.TOKEN_KEY) ? `Bearer ${localStorage.getItem(AUTH_CONFIG.TOKEN_KEY)}` : '',
      },
      body: JSON.stringify({
        answer_text: answerText // 发送答案字母作为文本
      })
    });
    
    // 解析响应
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.msg || `提交答案失败: ${response.status}`);
    }
    
    const data = await response.json();
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
  getActiveQuestions,
  submitAnswer,
  deactivateQuestion,
  getQuestionStats,
  getUserReport,
  getPresentationStats,
  generateQuestionsFromFile,
  getPresentationQuestions
};
