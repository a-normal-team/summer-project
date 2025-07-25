# WebSocket API 文档

## 概述

本文档描述了前后端使用的WebSocket API接口，用于实时通信功能。

## 连接和身份验证

所有的WebSocket连接都需要进行身份验证，我们通过在连接时提供JWT令牌来实现。

### 连接建立

客户端应该连接到WebSocket端点（服务器URL），连接后会收到服务器的连接确认。

### 加入演讲室

**客户端发送：**
```javascript
socket.emit('join', {
  presentation_id: 123,  // 演讲的ID
  token: 'your_jwt_token_here',  // JWT令牌
  role: 'listener'  // 角色：'speaker'或'listener'
});
```

**服务器响应：**
```javascript
// 成功
socket.on('joined', (data) => {
  // data: { presentation_id: 123, role: 'listener' }
});

// 失败
socket.on('error', (data) => {
  // data: { message: '错误信息' }
});
```

## 发送反馈（听众）

听众可以向演讲者发送实时反馈。

**客户端发送：**
```javascript
socket.emit('feedback', {
  presentationId: 123,  // 演讲的ID
  feedbackType: 'too_fast',  // 反馈类型
  content: '演讲速度太快，跟不上'  // 可选：详细反馈内容
});
```

**服务器响应：**
```javascript
// 成功
socket.on('feedback_result', (data) => {
  // data: { success: true, message: '反馈已发送给演讲者' }
});

// 失败
socket.on('error', (data) => {
  // data: { message: '错误信息' }
});
```

## 接收反馈（演讲者）

演讲者可以实时接收听众的反馈。

**演讲者监听：**
```javascript
socket.on('receive_feedback', (data) => {
  // data: { 
  //   id: 456,
  //   feedbackType: 'too_fast', 
  //   content: '可选的详细内容',
  //   timestamp: '2023-07-25T14:30:00.000Z',
  //   user_id: 789,
  //   username: '听众用户名'
  // }
});
```

## 问题相关事件

### 新问题通知

当演讲者创建新问题时，所有听众会收到通知。

**客户端监听：**
```javascript
socket.on('new_question', (data) => {
  // data: {
  //   id: 123,
  //   question_text: '问题内容',
  //   question_type: 'multiple_choice',
  //   options: ['选项1', '选项2', '选项3', '选项4'],
  //   is_active: true
  // }
});
```

### 问题统计更新

当有新的回答提交时，演讲者会收到问题统计数据的更新。

**客户端监听：**
```javascript
socket.on('question_stats_update', (data) => {
  // data: {
  //   question_id: 123,
  //   question_text: '问题内容',
  //   total_answers: 15,
  //   correct_answers: 10,
  //   correct_rate: '66.67%',
  //   option_distribution: {
  //     '选项1': 5,
  //     '选项2': 10,
  //     '选项3': 0,
  //     '选项4': 0
  //   }
  // }
});
```

### 问题停用通知

当演讲者停用问题时，所有听众会收到通知。

**客户端监听：**
```javascript
socket.on('question_deactivated', (data) => {
  // data: { 
  //   question_id: 123,
  //   presentation_id: 456
  // }
});
```

## 其他通知

### 房间信息

演讲者加入房间时会收到当前房间状态的信息。

**演讲者监听：**
```javascript
socket.on('room_info', (data) => {
  // data: { listeners_count: 15 }  // 当前房间内的听众数量
});
```

### 系统通知

系统会发送各种通知，如新听众加入等。

**客户端监听：**
```javascript
socket.on('notification', (data) => {
  // data: { 
  //   type: 'listener_joined', 
  //   message: '新听众加入' 
  // }
});
```
