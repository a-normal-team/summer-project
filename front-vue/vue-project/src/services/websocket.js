/**
 * WebSocket服务
 * 使用Socket.IO进行实时通信，如即时反馈、通知等
 */
import { io } from 'socket.io-client';

// Socket.IO实例
let socket = null;
let reconnectAttempts = 0;
const maxReconnectAttempts = 5;
const reconnectTimeout = 3000; // 3秒后重试

// 消息处理函数映射 (用于自定义事件处理)
const messageHandlers = {};

/**
 * 初始化Socket.IO连接
 * @param {string} presentationId - 演讲ID，用于创建针对特定演讲的连接
 * @param {string} userRole - 用户角色(listener/speaker/organizer)
 * @returns {Socket} Socket.IO实例
 */
export function initWebSocket(presentationId, userRole) {
  console.log(`初始化WebSocket连接: 演讲ID=${presentationId}, 角色=${userRole}`);
  // 如果已有连接，先关闭
  closeWebSocket();

  // 从本地存储获取令牌，尝试多种可能的令牌键
  let token = localStorage.getItem('token');
  if (!token) {
    const roleTokens = {
      speaker: localStorage.getItem('speaker_token'),
      listener: localStorage.getItem('listener_token'),
      organizer: localStorage.getItem('organizer_token')
    };
    token = roleTokens[userRole] || '';
  }

  // 确定Socket.IO服务器URL (从环境变量或使用默认值)
  const serverUrl = import.meta.env.VITE_WEBSOCKET_URL || `${window.location.protocol}//${window.location.hostname}:8080`;
  try {
    console.log(`尝试连接到Socket.IO服务器: ${serverUrl}`);
    socket = io(serverUrl, {
      reconnection: true,
      reconnectionAttempts: maxReconnectAttempts,
      reconnectionDelay: reconnectTimeout,
      query: { token: token },
      transports: ['websocket', 'polling'],
      withCredentials: false,
      forceNew: true,
      timeout: 10000,
      path: '/socket.io',
      extraHeaders: {
        'Origin': window.location.origin,
        'x-requested-with': 'XMLHttpRequest'
      }
    });

    // 监听所有事件，调试用
    socket.onAny((event, data) => {
      console.log('[ws调试] onAny事件:', event, data);
    });

    // 监听连接事件
    socket.on('connect', () => {
      console.log('[ws调试] 事件: connect', { socketId: socket.id });
      reconnectAttempts = 0;
      const joinData = {
        presentation_id: presentationId,
        token: token,
        role: userRole
      };
      console.log('[ws调试] 发送join事件，数据:', joinData);
      socket.emit('join', joinData);
    });
    socket.on('disconnect', (reason) => {
      console.log('[ws调试] 事件: disconnect', reason);
    });
    socket.on('connect_error', (error) => {
      console.log('[ws调试] 事件: connect_error', error);
    });
    socket.on('joined', (data) => {
      console.log('[ws调试] 事件: joined', data);
    });
    socket.on('error', (data) => {
      console.log('[ws调试] 事件: error', data);
    });
    socket.on('receive_feedback', (data) => {
      console.log('[ws调试] 事件: receive_feedback', data);
      if (messageHandlers['receive_feedback']) {
        messageHandlers['receive_feedback'](data);
      }
    });
    socket.on('feedback_result', (data) => {
      console.log('[ws调试] 事件: feedback_result', data);
      if (messageHandlers['feedback_result']) {
        messageHandlers['feedback_result'](data);
      }
    });
    socket.on('new_question', (data) => {
      console.log('[ws调试] 事件: new_question', data);
      if (messageHandlers['new_question']) {
        messageHandlers['new_question'](data);
      }
    });
    socket.on('question_stats_update', (data) => {
      console.log('[ws调试] 事件: question_stats_update', data);
      if (messageHandlers['question_stats_update']) {
        messageHandlers['question_stats_update'](data);
      }
    });
    return socket;
  } catch (err) {
    console.error('创建Socket.IO连接失败:', err);
    return null;
  }
}

/**
 * 关闭Socket.IO连接
 */
export function closeWebSocket() {
  if (socket) {
    socket.disconnect();
    socket = null;
  }
}

/**
 * 通过Socket.IO发送消息到服务器
 * @param {string} eventName - 事件名称
 * @param {Object} data - 消息数据
 * @returns {boolean} 是否成功发送
 */
export function sendMessage(eventName, data) {
  if (!socket || !socket.connected) {
    console.error('Socket.IO未连接，无法发送消息');
    return false;
  }
  
  try {
    // 添加时间戳到数据对象
    const messageData = {
      ...data,
      timestamp: new Date().toISOString()
    };
    
    // 在Socket.IO中直接使用事件名发送
    socket.emit(eventName, messageData);
    return true;
  } catch (err) {
    console.error(`发送Socket.IO消息(${eventName})失败:`, err);
    return false;
  }
}

/**
 * 注册消息处理函数
 * @param {string} eventName - 事件名称
 * @param {Function} handler - 处理函数
 */
export function registerMessageHandler(eventName, handler) {
  if (typeof handler === 'function') {
    messageHandlers[eventName] = handler;
    
    // 如果socket已存在，直接注册监听器
    if (socket) {
      socket.on(eventName, (data) => {
        console.log(`收到${eventName}事件:`, data);
        handler(data);
      });
    }
  }
}

/**
 * 发送即时反馈
 * @param {number} presentationId - 演讲ID
 * @param {string} feedbackType - 反馈类型
 * @param {string} content - 可选的附加内容
 * @returns {boolean} 是否成功发送
 */
export function sendFeedback(presentationId, feedbackType, content = '') {
  console.log(`尝试发送反馈: 演讲ID=${presentationId}, 类型=${feedbackType}`);
  
  // 尝试按照API文档格式化数据
  // 注意字段命名可能需要调整以符合后端API
  return sendMessage('feedback', {
    // 使用 presentationId 或 presentation_id 取决于后端API预期
    presentationId: presentationId,
    presentation_id: presentationId, // 添加下划线版本以兼容
    feedbackType: feedbackType,
    feedback_type: feedbackType, // 添加下划线版本以兼容
    content: content
  });
}
