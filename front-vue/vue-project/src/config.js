/**
 * 配置文件
 * 集中管理所有应用程序配置
 */

// API配置
export const API_CONFIG = {
  // API基础URL，可以根据环境变量设置不同的值
  BASE_URL: import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:5000/api',
  // 请求超时时间（毫秒）
  TIMEOUT: 10000,
};

// 认证配置
export const AUTH_CONFIG = {
  // 存储token的键名
  TOKEN_KEY: 'token',
  // token过期时间（毫秒）
  TOKEN_EXPIRY: 24 * 60 * 60 * 1000, // 24小时
};

// 应用配置
export const APP_CONFIG = {
  // 应用名称
  APP_NAME: 'AI Pop Quiz',
  // 版本
  VERSION: '1.0.0',
};
