/**
 * WebSocket连接管理模块
 * 处理与服务器的实时通信
 */

import { io } from "socket.io-client";
import { useAuthStore } from '@/stores/auth'; // 假设您有一个存储认证信息的store

let socket = null;
let isConnecting = false;
const listeners = {};

/**
 * 初始化WebSocket连接
 * @param {string} token - JWT认证令牌
 * @returns {Promise} - 返回连接结果的Promise
 */
export function initWebSocket(token) {
  return new Promise((resolve, reject) => {
    if (socket && socket.connected) {
      console.log("WebSocket已连接");
      resolve(socket);
      return;
    }

    if (isConnecting) {
      console.log("WebSocket正在连接中...");
      const checkInterval = setInterval(() => {
        if (socket && socket.connected) {
          clearInterval(checkInterval);
          resolve(socket);
        }
      }, 100);
      return;
    }

    isConnecting = true;
    
    // 从Auth Store获取token
    const authStore = useAuthStore();
    const tokenToUse = token || authStore.token;
    
    if (!tokenToUse) {
      isConnecting = false;
      reject(new Error("未提供认证令牌"));
      return;
    }
    
    console.log("正在连接WebSocket...");
    
    // 设置Socket.IO连接选项
    const options = {
      autoConnect: true,
      reconnection: true,
      reconnectionAttempts: 5,
      reconnectionDelay: 1000,
      query: { token: tokenToUse },
      transports: ['websocket', 'polling'],
      withCredentials: false,
    };
    
    // 确保URL正确包含协议和端口
    const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:5000';
    socket = io(apiUrl, options);
    
    // 连接事件处理
    socket.on('connect', () => {
      console.log("WebSocket连接成功");
      isConnecting = false;
      resolve(socket);
    });
    
    socket.on('connect_error', (error) => {
      console.error("WebSocket连接错误:", error);
      isConnecting = false;
      reject(error);
    });
    
    socket.on('disconnect', (reason) => {
      console.log(`WebSocket连接断开: ${reason}`);
    });
    
    // 注册全局错误处理
    socket.on('error', (data) => {
      console.error("WebSocket错误:", data.message);
    });
  });
}

/**
 * 加入演讲室
 * @param {number} presentationId - 演讲ID
 * @param {string} role - 用户角色：'speaker'或'listener'
 * @returns {Promise} - 返回加入结果的Promise
 */
export function joinPresentation(presentationId, role) {
  return new Promise((resolve, reject) => {
    if (!socket || !socket.connected) {
      reject(new Error("WebSocket未连接"));
      return;
    }
    
    const authStore = useAuthStore();
    
    socket.emit('join', {
      presentation_id: presentationId,
      token: authStore.token,
      role: role
    });
    
    // 等待加入成功响应
    socket.once('joined', (data) => {
      console.log(`成功加入演讲室 ${data.presentation_id}，角色: ${data.role}`);
      resolve(data);
    });
    
    // 处理可能的错误
    socket.once('error', (data) => {
      console.error(`加入演讲室失败: ${data.message}`);
      reject(new Error(data.message));
    });
    
    // 设置超时
    setTimeout(() => {
      reject(new Error("加入演讲室超时"));
    }, 5000);
  });
}

/**
 * 发送反馈
 * @param {number} presentationId - 演讲ID
 * @param {string} feedbackType - 反馈类型
 * @param {string} content - 反馈内容
 * @returns {Promise} - 返回发送结果的Promise
 */
export function sendFeedback(presentationId, feedbackType, content = "") {
  return new Promise((resolve, reject) => {
    if (!socket || !socket.connected) {
      reject(new Error("WebSocket未连接"));
      return;
    }
    
    socket.emit('feedback', {
      presentationId: presentationId,
      feedbackType: feedbackType,
      content: content
    });
    
    // 等待发送结果
    socket.once('feedback_result', (data) => {
      if (data.success) {
        resolve(data);
      } else {
        reject(new Error(data.message));
      }
    });
    
    // 处理可能的错误
    socket.once('error', (data) => {
      reject(new Error(data.message));
    });
    
    // 设置超时
    setTimeout(() => {
      reject(new Error("发送反馈超时"));
    }, 5000);
  });
}

/**
 * 添加事件监听器
 * @param {string} event - 事件名称
 * @param {function} callback - 回调函数
 */
export function addListener(event, callback) {
  if (!socket) {
    console.warn(`尝试为未连接的WebSocket添加${event}事件监听器`);
    return;
  }
  
  // 保存监听器引用以便后续移除
  if (!listeners[event]) {
    listeners[event] = [];
  }
  
  listeners[event].push(callback);
  socket.on(event, callback);
}

/**
 * 移除事件监听器
 * @param {string} event - 事件名称
 * @param {function} callback - 回调函数，如果不提供则移除所有该事件的监听器
 */
export function removeListener(event, callback) {
  if (!socket) return;
  
  if (callback && listeners[event]) {
    // 移除特定回调
    const idx = listeners[event].indexOf(callback);
    if (idx !== -1) {
      listeners[event].splice(idx, 1);
      socket.off(event, callback);
    }
  } else if (listeners[event]) {
    // 移除所有该事件监听器
    listeners[event].forEach(cb => socket.off(event, cb));
    listeners[event] = [];
  }
}

/**
 * 断开WebSocket连接
 */
export function disconnect() {
  if (socket) {
    socket.disconnect();
    socket = null;
  }
  isConnecting = false;
}
