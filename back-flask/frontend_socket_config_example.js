/**
 * WebSocket连接配置示例
 */

import { io } from "socket.io-client";

// 更新为新的端口号
const WEBSOCKET_URL = "http://localhost:8080";

const socket = io(WEBSOCKET_URL, {
  autoConnect: true,
  query: { token: "your-jwt-token" }
});

// 连接事件处理
socket.on('connect', () => {
  console.log("WebSocket连接成功");
});

// 其他事件监听...

export default socket;
