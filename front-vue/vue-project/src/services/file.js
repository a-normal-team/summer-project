/**
 * 文件服务
 * 提供与文件相关的API请求功能
 */

import { get } from './http';
import { API_CONFIG } from '../config';

/**
 * 上传文件
 * @param {File} file - 要上传的文件
 * @param {number} presentationId - 关联的演讲ID
 * @returns {Promise} - 包含上传结果的Promise
 */
export async function uploadFile(file, presentationId) {
  try {
    // 创建FormData对象
    const formData = new FormData();
    formData.append('file', file);
    
    // 如果提供了演讲ID，则添加到表单
    if (presentationId) {
      formData.append('presentation_id', presentationId);
    }
    
    // 获取存储的认证令牌
    const token = localStorage.getItem('token');
    
    // 设置请求选项
    const options = {
      method: 'POST',
      headers: token ? { 'Authorization': `Bearer ${token}` } : {},
      body: formData
    };
    
    // 发送请求
    const response = await fetch(`${API_CONFIG.BASE_URL}/files/upload`, options);
    
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.msg || '上传文件失败');
    }
    
    return await response.json();
  } catch (error) {
    console.error('上传文件失败:', error);
    throw error;
  }
}

/**
 * 获取演讲关联的文件列表
 * @param {number} presentationId - 演讲ID
 * @returns {Promise} - 包含文件列表的Promise
 */
export async function getFilesByPresentation(presentationId) {
  try {
    const data = await get(`/files/files_by_presentation/${presentationId}`);
    return data;
  } catch (error) {
    console.error(`获取演讲(ID: ${presentationId})关联的文件列表失败:`, error);
    throw error;
  }
}

/**
 * 获取文件下载URL
 * @param {number} fileId - 文件ID
 * @returns {string} - 文件下载URL
 */
export function getFileDownloadUrl(fileId) {
  return `${API_CONFIG.BASE_URL}/files/download/${fileId}`;
}
