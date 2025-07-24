/**
 * HTTP 客户端服务
 * 提供封装好的 fetch API，自动处理认证和错误
 */

import { API_CONFIG } from '../config';
import { getAuthToken } from './token';

/**
 * 执行 HTTP 请求
 * @param {string} endpoint - API 端点路径
 * @param {Object} options - 请求选项
 * @returns {Promise} - 包含请求结果的 Promise
 */
export async function apiRequest(endpoint, options = {}) {
  // 处理 endpoint，保留原始格式
  const cleanEndpoint = endpoint;
    
  const url = `${API_CONFIG.BASE_URL}${cleanEndpoint}`;
  
  // 获取最新的令牌
  const token = getAuthToken();
  
  // 设置默认请求头
  const headers = {
    'Content-Type': 'application/json',
    ...options.headers
  };
  
  // 如果有认证令牌，则添加到请求头
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }
  
  // 合并选项
  const requestOptions = {
    ...options,
    headers
  };
  
  try {
    console.log(`发送请求到: ${url}`);
    const response = await fetch(url, requestOptions);
    console.log(`收到响应: `, response);
    
    // 处理重定向
    if (response.status === 308 || response.status === 307) {
      console.warn(`收到重定向状态码(${response.status})，正在处理重定向`);
      
      // 获取重定向位置
      const redirectUrl = response.headers.get('Location');
      if (redirectUrl) {
        console.log(`重定向到: ${redirectUrl}`);
        
        // 对于重定向，自动跟随重定向URL
        const redirectResponse = await fetch(redirectUrl, requestOptions);
        
        if (!redirectResponse.ok && redirectResponse.status !== 204) {
          throw new Error(`重定向后请求失败: ${redirectResponse.status}`);
        }
        
        // 对于204状态码(No Content)，返回空对象
        if (redirectResponse.status === 204) {
          return {};
        }
        
        // 解析重定向响应
        const contentType = redirectResponse.headers.get('content-type');
        if (contentType && contentType.includes('application/json')) {
          return await redirectResponse.json();
        } else {
          return await redirectResponse.text();
        }
      }
    }
    
    // 尝试解析 JSON 响应
    let data;
    const contentType = response.headers.get('content-type');
    if (contentType && contentType.includes('application/json')) {
      data = await response.json();
    } else {
      data = await response.text();
    }
    
    // 检查响应状态
    if (!response.ok) {
      // 处理认证错误
      if (response.status === 401) {
        // 如果令牌已过期或无效，清除存储的令牌
        localStorage.removeItem('token');
      }
      
      throw new Error(data.msg || '请求失败');
    }
    
    return data;
  } catch (error) {
    if (error.name === 'TypeError' && error.message === 'Failed to fetch') {
      console.error(`无法连接到API服务器(${API_CONFIG.BASE_URL})，请确保后端服务正在运行`);
      throw new Error(`无法连接到服务器(${API_CONFIG.BASE_URL.split('/api')[0]})，请确保后端服务正在运行`);
    }
    
    console.error('API 请求错误:', error);
    throw error;
  }
}

/**
 * 发起 GET 请求
 * @param {string} endpoint - API 端点路径
 * @param {Object} options - 额外的请求选项
 * @returns {Promise} - 包含请求结果的 Promise
 */
export function get(endpoint, options = {}) {
  return apiRequest(endpoint, {
    ...options,
    method: 'GET'
  });
}

/**
 * 发起 POST 请求
 * @param {string} endpoint - API 端点路径
 * @param {Object} body - 请求体数据
 * @param {Object} options - 额外的请求选项
 * @returns {Promise} - 包含请求结果的 Promise
 */
export function post(endpoint, body, options = {}) {
  return apiRequest(endpoint, {
    ...options,
    method: 'POST',
    body: JSON.stringify(body)
  });
}

/**
 * 发起 PUT 请求
 * @param {string} endpoint - API 端点路径
 * @param {Object} body - 请求体数据
 * @param {Object} options - 额外的请求选项
 * @returns {Promise} - 包含请求结果的 Promise
 */
export function put(endpoint, body, options = {}) {
  return apiRequest(endpoint, {
    ...options,
    method: 'PUT',
    body: JSON.stringify(body)
  });
}

/**
 * 发起 DELETE 请求
 * @param {string} endpoint - API 端点路径
 * @param {Object} options - 额外的请求选项
 * @returns {Promise} - 包含请求结果的 Promise
 */
export function del(endpoint, options = {}) {
  return apiRequest(endpoint, {
    ...options,
    method: 'DELETE'
  });
}
