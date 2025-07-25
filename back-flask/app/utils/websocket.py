"""
WebSocket服务模块
处理实时通信，如即时反馈、通知等
"""

import json
import logging
from datetime import datetime
from flask import current_app, request
from flask_socketio import emit, join_room, leave_room
from flask_jwt_extended import decode_token, exceptions
from app.models import User, Presentation, db, Feedback  # 导入数据库模型

# 创建日志记录器
logger = logging.getLogger(__name__)

# 存储连接的客户端
connected_clients = {}
# 存储演讲室信息 {presentation_id: {speaker_sid: sid, listeners: [sid1, sid2, ...]}}
presentation_rooms = {}


def init_socketio(socketio):
    """初始化SocketIO并注册事件处理函数"""
    
    @socketio.on('connect')
    def handle_connect():
        """处理客户端连接"""
        logger.info(f"客户端连接: {request.sid}")
        
        # 尝试从请求参数中获取token
        token = request.args.get('token')
        if token:
            try:
                # 验证token
                token_data = decode_token(token)
                user_id = token_data['sub']
                logger.info(f"用户 {user_id} 连接成功")
                # 保存用户信息
                connected_clients[request.sid] = {
                    'user_id': user_id,
                    'joined_at': datetime.utcnow()
                }
                return True
            except exceptions.PyJWTError as e:
                logger.error(f"Token验证失败: {str(e)}")
                return False
        else:
            # 允许未认证连接，稍后可以通过join事件进行认证
            logger.warning(f"客户端 {request.sid} 未提供token")
            return True
    
    @socketio.on('disconnect')
    def handle_disconnect():
        """处理客户端断开连接"""
        sid = request.sid
        logger.info(f"客户端断开连接: {sid}")
        
        # 清理客户端信息
        if sid in connected_clients:
            client_info = connected_clients[sid]
            presentation_id = client_info.get('presentation_id')
            role = client_info.get('role')
            
            if presentation_id and presentation_id in presentation_rooms:
                room_info = presentation_rooms[presentation_id]
                
                # 如果是演讲者，移除演讲者信息
                if role == 'speaker' and room_info.get('speaker_sid') == sid:
                    room_info['speaker_sid'] = None
                    logger.info(f"演讲 {presentation_id} 的演讲者已断开连接")
                
                # 如果是听众，从听众列表中移除
                elif role == 'listener' and sid in room_info.get('listeners', []):
                    room_info['listeners'].remove(sid)
                    logger.info(f"听众已离开演讲 {presentation_id}")
            
            # 删除客户端记录
            del connected_clients[sid]
    
    @socketio.on('join')
    def handle_join(data):
        """处理加入演讲室"""
        try:
            presentation_id = data.get('presentation_id')
            token = data.get('token')
            role = data.get('role', 'listener')
            
            if not presentation_id or not token:
                emit('error', {'message': '缺少必要参数'})
                return
            
            # 验证token
            try:
                token_data = decode_token(token)
                user_id = token_data['sub']
            except exceptions.PyJWTError as e:
                logger.error(f"无效的令牌: {str(e)}")
                emit('error', {'message': '无效的令牌'})
                return
            
            # 验证演讲ID
            presentation = Presentation.query.get(presentation_id)
            if not presentation:
                emit('error', {'message': '演讲不存在'})
                return
            
            # 加入房间
            join_room(f"presentation_{presentation_id}")
            
            # 存储客户端信息
            connected_clients[request.sid] = {
                'user_id': user_id,
                'presentation_id': presentation_id,
                'role': role,
                'joined_at': datetime.utcnow()
            }
            
            # 更新演讲室信息
            if presentation_id not in presentation_rooms:
                presentation_rooms[presentation_id] = {
                    'speaker_sid': None,
                    'listeners': []
                }
            
            room_info = presentation_rooms[presentation_id]
            
            if role == 'speaker':
                # 如果已有演讲者，通知该演讲者有新的演讲者连接
                if room_info['speaker_sid']:
                    emit('notification', {
                        'type': 'speaker_changed',
                        'message': '另一个演讲者已连接'
                    }, room=room_info['speaker_sid'])
                
                room_info['speaker_sid'] = request.sid
                logger.info(f"演讲者加入演讲 {presentation_id}")
                
                # 通知演讲者当前有多少听众
                emit('room_info', {
                    'listeners_count': len(room_info.get('listeners', []))
                })
            elif role == 'listener':
                room_info.setdefault('listeners', []).append(request.sid)
                logger.info(f"听众加入演讲 {presentation_id}")
                
                # 如果有演讲者，通知演讲者有新的听众
                if room_info['speaker_sid']:
                    emit('notification', {
                        'type': 'listener_joined',
                        'message': '新听众加入'
                    }, room=room_info['speaker_sid'])
            
            # 通知客户端加入成功
            emit('joined', {
                'presentation_id': presentation_id,
                'role': role
            })
            
        except Exception as e:
            logger.error(f"加入演讲室时发生错误: {str(e)}")
            emit('error', {'message': '服务器错误'})
    
    @socketio.on('feedback')
    def handle_feedback(data):
        """处理听众反馈"""
        try:
            sid = request.sid
            
            if sid not in connected_clients:
                emit('error', {'message': '未授权'})
                return
            
            client_info = connected_clients[sid]
            presentation_id = data.get('presentationId') or client_info.get('presentation_id')
            feedback_type = data.get('feedbackType')
            feedback_content = data.get('content', '')
            
            if not presentation_id or not feedback_type:
                emit('error', {'message': '缺少必要参数'})
                return
            
            if presentation_id not in presentation_rooms:
                emit('error', {'message': '演讲室不存在'})
                return
            
            # 获取演讲者的sid
            speaker_sid = presentation_rooms[presentation_id].get('speaker_sid')
            
            # 获取反馈发送者信息
            user_id = client_info.get('user_id')
            user = User.query.get(user_id)
            username = user.username if user else "匿名用户"
            
            # 保存反馈到数据库
            new_feedback = Feedback(
                presentation_id=presentation_id,
                user_id=user_id,
                feedback_type=feedback_type,
                content=feedback_content
            )
            db.session.add(new_feedback)
            db.session.commit()
            
            feedback_data = {
                'id': new_feedback.id,
                'feedbackType': feedback_type,
                'content': feedback_content,
                'timestamp': datetime.utcnow().isoformat(),
                'user_id': user_id,
                'username': username
            }
            
            if not speaker_sid:
                logger.warning(f"演讲 {presentation_id} 没有在线的演讲者，反馈已保存但未实时发送")
                emit('feedback_result', {
                    'success': True,
                    'message': '演讲者不在线，反馈已记录'
                })
                return
            
            # 向演讲者发送反馈
            emit('receive_feedback', feedback_data, room=speaker_sid)
            
            # 通知发送者反馈已发送
            emit('feedback_result', {
                'success': True,
                'message': '反馈已发送给演讲者'
            })
            
            logger.info(f"听众 {username}({user_id}) 向演讲 {presentation_id} 发送了反馈: {feedback_type}")
            
        except Exception as e:
            logger.error(f"处理反馈时发生错误: {str(e)}")
            emit('error', {'message': '服务器错误'})

    return socketio
