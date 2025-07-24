/**
 * 令牌工具
 * 提供应用程序范围内的令牌管理功能
 */

import { AUTH_CONFIG } from '../config';

/**
 * 获取当前标签页的认证令牌
 * 使用基于会话存储的令牌管理，确保每个标签页使用自己的令牌
 * @returns {string|null} 获取到的认证令牌或null
 */
export function getAuthToken() {
  // 为确保每个标签页独立，我们使用会话标识符
  let sessionId = sessionStorage.getItem('browserTabSessionId');
  if (!sessionId) {
    // 如果当前标签页没有会话ID，生成一个唯一标识符
    sessionId = 'tab_' + new Date().getTime() + '_' + Math.random().toString(36).substring(2, 15);
    sessionStorage.setItem('browserTabSessionId', sessionId);
    console.log(`[令牌管理] 为当前标签页创建新的会话ID: ${sessionId}`);
  }

  // 从会话存储中获取此标签页专用的认证信息
  const sessionUserRole = sessionStorage.getItem('sessionUserRole');
  const sessionUserIdentifier = sessionStorage.getItem('sessionUserIdentifier');
  const sessionTokenKey = sessionStorage.getItem('sessionTokenKey');
  const sessionToken = sessionStorage.getItem('sessionToken');
  
  // 如果会话存储中有有效的令牌，直接使用
  if (sessionToken) {
    console.log(`[令牌管理] 使用标签页专用令牌 (${sessionUserRole}/${sessionUserIdentifier})`);
    return sessionToken;
  }
  
  // 如果会话存储中没有令牌但有令牌键，尝试从localStorage获取
  if (sessionTokenKey) {
    const token = localStorage.getItem(sessionTokenKey);
    if (token) {
      // 存入会话存储以便后续使用
      sessionStorage.setItem('sessionToken', token);
      console.log(`[令牌管理] 从localStorage获取并缓存标签页专用令牌`);
      return token;
    }
  }
  
  // 如果没有标签页特定的令牌信息，尝试从localStorage获取当前配置
  const currentUserTokenKey = localStorage.getItem('currentUserTokenKey');
  let token = currentUserTokenKey ? localStorage.getItem(currentUserTokenKey) : null;
  
  if (token) {
    // 保存到会话存储中
    const currentRole = localStorage.getItem('currentUserRole');
    const currentUserId = localStorage.getItem('currentUserIdentifier');
    
    sessionStorage.setItem('sessionUserRole', currentRole);
    sessionStorage.setItem('sessionUserIdentifier', currentUserId);
    sessionStorage.setItem('sessionTokenKey', currentUserTokenKey);
    sessionStorage.setItem('sessionToken', token);
    
    console.log(`[令牌管理] 从localStorage加载令牌到会话 (${currentRole}/${currentUserId})`);
    return token;
  }
  
  // 如果前面的方法都失败，尝试使用通用令牌（兼容模式）
  token = localStorage.getItem(AUTH_CONFIG.TOKEN_KEY);
  if (token) {
    console.log('[令牌管理] 使用通用令牌');
    return token;
  }
  
  console.log('[令牌管理] 无法获取有效令牌');
  return null;
}

/**
 * 将令牌信息保存到会话存储中
 * @param {string} token - 认证令牌
 * @param {string} tokenKey - 令牌键
 * @param {string} userRole - 用户角色
 * @param {string} userId - 用户标识符
 */
export function saveTokenToSession(token, tokenKey, userRole, userId) {
  // 确保会话ID存在
  let sessionId = sessionStorage.getItem('browserTabSessionId');
  if (!sessionId) {
    sessionId = 'tab_' + new Date().getTime() + '_' + Math.random().toString(36).substring(2, 15);
    sessionStorage.setItem('browserTabSessionId', sessionId);
  }
  
  // 保存认证信息到会话存储
  sessionStorage.setItem('sessionUserRole', userRole);
  sessionStorage.setItem('sessionUserIdentifier', userId);
  sessionStorage.setItem('sessionTokenKey', tokenKey);
  sessionStorage.setItem('sessionToken', token);
  
  console.log(`[令牌管理] 保存令牌到会话 (${userRole}/${userId})`);
}

/**
 * 清除会话存储中的令牌信息
 */
export function clearSessionToken() {
  sessionStorage.removeItem('sessionUserRole');
  sessionStorage.removeItem('sessionUserIdentifier');
  sessionStorage.removeItem('sessionTokenKey');
  sessionStorage.removeItem('sessionToken');
  
  console.log('[令牌管理] 已清除会话令牌');
}
