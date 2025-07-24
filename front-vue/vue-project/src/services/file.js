/**
 * 文件服务
 * 提供与文件相关的API请求功能
 */

import { get } from './http';
import { API_CONFIG } from '../config';
import { getAuthToken } from './token';

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
    
    // 获取当前标签页的认证令牌
    const token = getAuthToken();
    
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

/**
 * 删除文件
 * @param {number} fileId - 要删除的文件ID
 * @returns {Promise} - 包含删除结果的Promise
 * @description 仅组织者或文件原始上传者有权限删除文件
 */
export async function deleteFile(fileId) {
  try {
    // 获取当前标签页的认证令牌
    const token = getAuthToken();
    if (!token) {
      throw new Error('未登录，无法删除文件');
    }
    
    // 设置请求选项，包含授权头
    const options = {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    };
    
    // 发送请求，根据API文档，删除文件的URL为/api/files/delete/<int:file_id>
    const response = await fetch(`${API_CONFIG.BASE_URL}/files/delete/${fileId}`, options);
    
    if (!response.ok) {
      if (response.status === 403) {
        throw new Error('无权限删除此文件');
      } else if (response.status === 404) {
        throw new Error('文件不存在');
      }
      const errorData = await response.json();
      throw new Error(errorData.msg || '删除文件失败');
    }
    
    return await response.json();
  } catch (error) {
    console.error('删除文件失败:', error);
    throw error;
  }
}

/**
 * 下载文件
 * @param {number} fileId - 文件ID
 * @returns {Promise} - 包含下载结果的Promise
 */
export async function downloadFile(fileId) {
  try {
    // 获取当前标签页的认证令牌
    const token = getAuthToken();
    if (!token) {
      throw new Error('未登录，无法下载文件');
    }
    
    // 设置请求选项，包含授权头
    const options = {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`
      }
    };
    
    // 发送请求
    const response = await fetch(`${API_CONFIG.BASE_URL}/files/download/${fileId}`, options);
    
    if (!response.ok) {
      if (response.status === 401 || response.status === 403) {
        throw new Error('无权限下载此文件');
      }
      const errorData = await response.json();
      throw new Error(errorData.msg || '下载文件失败');
    }
    
    // 获取文件blob
    const blob = await response.blob();
    
    // 从响应头中获取文件名
    let filename = 'download';
    const contentDisposition = response.headers.get('Content-Disposition');
    if (contentDisposition) {
      const filenameMatch = contentDisposition.match(/filename="(.+)"/);
      if (filenameMatch) {
        filename = filenameMatch[1];
      }
    }
    
    // 创建下载链接
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    
    // 触发下载
    document.body.appendChild(link);
    link.click();
    
    // 清理
    setTimeout(() => {
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);
    }, 100);
    
    return { success: true };
  } catch (error) {
    console.error('下载文件失败:', error);
    throw error;
  }
}
