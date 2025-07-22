# AI Pop Quiz 后端 API 文档

本文档详细描述了 AI Pop Quiz 后端应用提供的 RESTful API 接口。

**基础 URL**: `http://127.0.0.1:5000/api`

## 认证 (Auth)

### 1. 用户注册
*   **URL**: `/auth/register`
*   **方法**: `POST`
*   **描述**: 注册新用户。
*   **请求体示例**:
    ```json
    {
        "username": "new_user",
        "password": "secure_password",
        "role": "listener" // 可选，默认为 "listener"。可选值: "organizer", "speaker", "listener"
    }
    ```
*   **响应体示例 (成功)**:
    ```json
    {
        "msg": "User registered successfully",
        "user_id": 1
    }
    ```
*   **响应体示例 (失败 - 用户名已存在)**:
    ```json
    {
        "msg": "Username already exists"
    }
    ```

### 2. 用户登录
*   **URL**: `/auth/login`
*   **方法**: `POST`
*   **描述**: 用户登录并获取 JWT 访问令牌。
*   **请求体示例**:
    ```json
    {
        "username": "existing_user",
        "password": "secure_password"
    }
    ```
*   **响应体示例 (成功)**:
    ```json
    {
        "msg": "Login successful",
        "access_token": "your_jwt_access_token"
    }
    ```
*   **响应体示例 (失败 - 凭据无效)**:
    ```json
    {
        "msg": "Invalid credentials"
    }
    ```

### 3. 获取用户资料
*   **URL**: `/auth/profile`
*   **方法**: `GET`
*   **描述**: 获取当前登录用户的资料。
*   **权限**: 需要有效的 JWT 访问令牌。
*   **响应体示例 (成功)**:
    ```json
    {
        "id": 1,
        "username": "testuser",
        "role": "listener"
    }
    ```
*   **响应体示例 (失败 - 用户未找到)**:
    ```json
    {
        "msg": "User not found"
    }
    ```

## 演示文稿 (Presentations)

### 1. 创建演示文稿
*   **URL**: `/presentations/`
*   **方法**: `POST`
*   **描述**: 演讲者创建新的演示文稿。
*   **权限**: 需要有效的 JWT 访问令牌，且用户角色为 `speaker`。
*   **请求体示例**:
    ```json
    {
        "title": "我的第一次演讲",
        "description": "这是一个关于 Flask 基础的介绍性演讲。"
    }
    ```
*   **响应体示例 (成功)**:
    ```json
    {
        "msg": "Presentation created successfully",
        "presentation_id": 1
    }
    ```

### 2. 获取所有演示文稿
*   **URL**: `/presentations`
*   **方法**: `GET`
*   **描述**: 获取所有可用的演示文稿列表。
*   **权限**: 需要有效的 JWT 访问令牌。
*   **响应体示例**:
    ```json
    [
        {
            "id": 1,
            "title": "我的第一次演讲",
            "description": "这是一个关于 Flask 基础的介绍性演讲。",
            "speaker_id": 1,
            "speaker_username": "speaker_one"
        }
    ]
    ```

### 3. 获取单个演示文稿
*   **URL**: `/presentations/<int:presentation_id>`
*   **方法**: `GET`
*   **描述**: 获取指定 ID 的演示文稿详情。
*   **权限**: 需要有效的 JWT 访问令牌。
*   **响应体示例 (成功)**:
    ```json
    {
        "id": 1,
        "title": "我的第一次演讲",
        "description": "这是一个关于 Flask 基础的介绍性演讲。",
        "speaker_id": 1,
        "speaker_username": "speaker_one"
    }
    ```
*   **响应体示例 (失败 - 未找到)**:
    ```json
    {
        "msg": "Presentation not found"
    }
    ```

### 4. 更新演示文稿
*   **URL**: `/presentations/<int:presentation_id>`
*   **方法**: `PUT`
*   **描述**: 演讲者更新指定演示文稿的信息。
*   **权限**: 需要有效的 JWT 访问令牌，且用户角色为 `speaker` (该演示文稿的演讲者) 或 `organizer`。
*   **请求体示例**:
    ```json
    {
        "title": "更新后的演讲标题",
        "description": "这是更新后的描述。"
    }
    ```
*   **响应体示例 (成功)**:
    ```json
    {
        "msg": "Presentation updated successfully"
    }
    ```
*   **响应体示例 (失败 - 未找到)**:
    ```json
    {
        "msg": "Presentation not found"
    }
    ```
*   **响应体示例 (失败 - 未授权)**:
    ```json
    {
        "msg": "Unauthorized to update this presentation"
    }
    ```

### 5. 删除演示文稿
*   **URL**: `/presentations/<int:presentation_id>`
*   **方法**: `DELETE`
*   **描述**: 演讲者删除指定演示文稿。
*   **权限**: 需要有效的 JWT 访问令牌，且用户角色为 `speaker` (该演示文稿的演讲者) 或 `organizer`。
*   **响应体示例 (成功)**:
    ```json
    {
        "msg": "Presentation deleted successfully"
    }
    ```
*   **响应体示例 (失败 - 未找到)**:
    ```json
    {
        "msg": "Presentation not found"
    }
    ```
*   **响应体示例 (失败 - 未授权)**:
    ```json
    {
        "msg": "Unauthorized to delete this presentation"
    }
    ```

### 6. 添加听众到演示文稿
*   **URL**: `/presentations/<int:presentation_id>/add_listener`
*   **方法**: `POST`
*   **描述**: 组织者或演讲者将听众添加到指定演示文稿，或听众将自己添加到演示文稿。
*   **权限**: 需要有效的 JWT 访问令牌，且满足以下条件之一：
    - 用户角色为 `organizer`
    - 用户角色为 `speaker` 且是该演示文稿的创建者
    - 用户角色为 `listener` (只能添加自己)
*   **请求体示例 (组织者或演讲者)**:
    ```json
    {
        "listener_id": 2 // 要添加的听众用户 ID
    }
    ```
*   **请求体示例 (听众)**:
    ```json
    {} // 听众不需要提供listener_id，会自动使用当前用户ID
    ```
*   **响应体示例 (成功)**:
    ```json
    {
        "msg": "Listener added to presentation successfully"
    }
    ```
*   **响应体示例 (失败 - 演示文稿未找到)**:
    ```json
    {
        "msg": "Presentation not found"
    }
    ```
*   **响应体示例 (失败 - 听众未找到或角色不符)**:
    ```json
    {
        "msg": "Listener not found or not a listener role"
    }
    ```
*   **响应体示例 (失败 - 已关联)**:
    ```json
    {
        "msg": "Listener already associated with this presentation"
    }
    ```
*   **响应体示例 (失败 - 未授权)**:
    ```json
    {
        "msg": "Unauthorized to add listener to this presentation"
    }
    ```

### 7. 从演示文稿中移除听众
*   **URL**: `/presentations/<int:presentation_id>/remove_listener`
*   **方法**: `POST`
*   **描述**: 组织者或演讲者从指定演示文稿中移除听众。
*   **权限**: 需要有效的 JWT 访问令牌，且用户角色为 `organizer` 或 `speaker` (该演示文稿的创建者)。
*   **请求体示例**:
    ```json
    {
        "listener_id": 2 // 要移除的听众用户 ID
    }
    ```
*   **响应体示例 (成功)**:
    ```json
    {
        "msg": "Listener removed from presentation successfully"
    }
    ```
*   **响应体示例 (失败 - 演示文稿未找到)**:
    ```json
    {
        "msg": "Presentation not found"
    }
    ```
*   **响应体示例 (失败 - 听众未找到或角色不符)**:
    ```json
    {
        "msg": "Listener not found or not a listener role"
    }
    ```
*   **响应体示例 (失败 - 未关联)**:
    ```json
    {
        "msg": "Listener not associated with this presentation"
    }
    ```
*   **响应体示例 (失败 - 未授权)**:
    ```json
    {
        "msg": "Unauthorized to remove listener from this presentation"
    }
    ```

## 测验 (Quiz)

### 1. 创建题目
*   **URL**: `/quiz/presentations/<int:presentation_id>/questions`
*   **方法**: `POST`
*   **描述**: 演讲者为指定演讲创建新题目。
*   **权限**: 需要有效的 JWT 访问令牌，且用户角色为 `speaker` 且是该演讲的演讲者。
*   **请求体示例**:
    ```json
    {
        "question_text": "Flask 是一个什么类型的框架？",
        "question_type": "multiple_choice",
        "options": ["微框架", "全栈框架", "前端框架", "数据库框架"],
        "correct_answer": "微框架"
    }
    ```
*   **响应体示例 (成功)**:
    ```json
    {
        "msg": "Question created successfully",
        "question_id": 1
    }
    ```

### 2. 获取活跃题目
*   **URL**: `/quiz/presentations/<int:presentation_id>/active_question`
*   **方法**: `GET`
*   **描述**: 获取指定演讲当前活跃的题目。
*   **权限**: 需要有效的 JWT 访问令牌，且用户是该演讲的 `listener` 或 `speaker`。
*   **响应体示例 (成功)**:
    ```json
    {
        "id": 1,
        "question_text": "Flask 是一个什么类型的框架？",
        "question_type": "multiple_choice",
        "options": ["微框架", "全栈框架", "前端框架", "数据库框架"]
    }
    ```
*   **响应体示例 (无活跃题目)**:
    ```json
    {
        "msg": "No active question for this presentation"
    }
    ```

### 3. 提交答案
*   **URL**: `/quiz/questions/<int:question_id>/answer`
*   **方法**: `POST`
*   **描述**: 听众提交对指定题目的答案。
*   **权限**: 需要有效的 JWT 访问令牌，且用户角色为 `listener`。
*   **请求体示例**:
    ```json
    {
        "answer_text": "A"
    }
    ```
*   **响应体示例 (成功 - 答案正确)**:
    ```json
    {
        "msg": "Answer submitted successfully",
        "answer_id": 1,
        "is_correct": true
    }
    ```
*   **响应体示例 (成功 - 答案错误)**:
    ```json
    {
        "msg": "Answer submitted successfully",
        "answer_id": 1,
        "is_correct": false
    }
    ```
*   **响应体示例 (已回答)**:
    ```json
    {
        "msg": "You have already answered this question"
    }
    ```

### 4. 停用题目
*   **URL**: `/quiz/questions/<int:question_id>/deactivate`
*   **方法**: `POST`
*   **描述**: 演讲者停用指定题目，使其不再接受答案。
*   **权限**: 需要有效的 JWT 访问令牌，且用户角色为 `speaker` (该题目所属演讲的演讲者) 或 `organizer`。
*   **响应体示例 (成功)**:
    ```json
    {
        "msg": "Question deactivated successfully"
    }
    ```

### 5. 获取题目统计
*   **URL**: `/quiz/questions/<int:question_id>/stats`
*   **方法**: `GET`
*   **描述**: 获取指定题目的作答统计（回答人数、正确率、选项分布等）。
*   **权限**: 需要有效的 JWT 访问令牌，且用户角色为 `speaker` (该题目所属演讲的演讲者) 或 `organizer`。
*   **响应体示例**:
    ```json
    {
        "question_id": 1,
        "question_text": "Flask 是一个什么类型的框架？",
        "total_answers": 5,
        "correct_answers": 3,
        "correct_rate": "60.00%",
        "option_distribution": {
            "微框架": 3,
            "全栈框架": 1,
            "前端框架": 1
        }
    }
    ```

### 6. 获取听众个人报告
*   **URL**: `/quiz/presentations/<int:presentation_id>/report/<int:user_id>`
*   **方法**: `GET`
*   **描述**: 获取指定听众在某个演讲中的个人作答报告。
*   **权限**: 需要有效的 JWT 访问令牌，且满足以下条件之一：
    - 听众只能查看自己的报告
    - 组织者可以查看任何听众的报告
    - 演讲者可以查看其演讲关联的听众报告
*   **响应体示例**:
    ```json
    {
        "listener_id": 2,
        "listener_username": "listener_one",
        "presentation_id": 1,
        "presentation_title": "我的第一次演讲",
        "total_questions_in_presentation": 2,
        "answered_questions": 2,
        "correct_answers": 1,
        "accuracy_rate": "50.00%",
        "question_details": [
            {
                "question_id": 1,
                "question_text": "Flask 是一个什么类型的框架？",
                "your_answer": "微框架",
                "is_correct": true,
                "correct_answer": "微框架"
            },
            {
                "question_id": 2,
                "question_text": "Python 的创始人是谁？",
                "your_answer": "James Gosling",
                "is_correct": false,
                "correct_answer": "Guido van Rossum"
            }
        ]
    }
    ```

### 7. 获取演讲整体统计
*   **URL**: `/quiz/presentations/<int:presentation_id>/overall_stats`
*   **方法**: `GET`
*   **描述**: 组织者查看某个演讲的整体互动数据（参与人数、平均正确率等）。
*   **权限**: 需要有效的 JWT 访问令牌，且用户角色为 `organizer`。
*   **响应体示例**:
    ```json
    {
        "presentation_id": 1,
        "presentation_title": "我的第一次演讲",
        "total_participants": 3,
        "total_questions_in_presentation": 2,
        "total_answers_submitted": 6,
        "average_correct_rate_across_all_questions": "66.67%",
        "listener_performance": [
            {
                "listener_id": 2,
                "listener_username": "listener_one",
                "answered_questions": 2,
                "correct_answers": 1,
                "accuracy_rate": "50.00%"
            },
            {
                "listener_id": 3,
                "listener_username": "listener_two",
                "answered_questions": 2,
                "correct_answers": 2,
                "accuracy_rate": "100.00%"
            }
        ]
    }
    ```

### 8. 从文件生成题目
*   **URL**: `/quiz/generate_questions`
*   **方法**: `POST`
*   **描述**: 演讲者根据上传的文件内容生成测验题目。
*   **权限**: 需要有效的 JWT 访问令牌，且用户角色为 `speaker`。
*   **请求体示例**:
    ```json
    {
        "file_id": 1,          // 要生成题目的文件 ID
        "presentation_id": 1   // 题目将关联的演讲 ID
    }
    ```
*   **响应体示例 (成功)**:
    ```json
    {
        "msg": "Successfully generated 3 questions",
        "question_ids": [1, 2, 3]
    }
    ```
*   **响应体示例 (失败 - 参数缺失)**:
    ```json
    {
        "msg": "file_id and presentation_id are required"
    }
    ```
*   **响应体示例 (失败 - 文件未找到)**:
    ```json
    {
        "msg": "File not found"
    }
    ```
*   **响应体示例 (失败 - 未授权使用文件)**:
    ```json
    {
        "msg": "Unauthorized to use this file"
    }
    ```
*   **响应体示例 (失败 - 演讲未找到)**:
    ```json
    {
        "msg": "Presentation not found"
    }
    ```
*   **响应体示例 (失败 - 未授权演讲)**:
    ```json
    {
        "msg": "You are not the speaker of this presentation"
    }
    ```
*   **响应体示例 (失败 - LLM API 未配置)**:
    ```json
    {
        "msg": "LLM API URL not configured"
    }
    ```
*   **响应体示例 (失败 - 文件无提取文本)**:
    ```json
    {
        "msg": "No extracted text content found for this file"
    }
    ```
*   **响应体示例 (失败 - LLM 生成失败)**:
    ```json
    {
        "msg": "Failed to generate questions from LLM: <error_details>"
    }
    ```

## 即时反馈 (Feedback)

### 1. 提交即时反馈
*   **URL**: `/feedback/presentations/<int:presentation_id>/submit`
*   **方法**: `POST`
*   **描述**: 听众提交预设的即时反馈。
*   **权限**: 需要有效的 JWT 访问令牌，且用户角色为 `listener` 且是该演讲的听众。
*   **请求体示例**:
    ```json
    {
        "feedback_type": "too_fast" // 可选值: "too_fast", "too_slow", "boring", "bad_question"
    }
    ```
*   **响应体示例 (成功)**:
    ```json
    {
        "msg": "Feedback submitted successfully",
        "feedback_id": 1
    }
    ```

### 2. 获取反馈统计
*   **URL**: `/feedback/presentations/<int:presentation_id>/stats`
*   **方法**: `GET`
*   **描述**: 演讲者或组织者查看指定演讲的即时反馈统计。
*   **权限**: 需要有效的 JWT 访问令牌，且用户角色为 `speaker` (该演讲的演讲者) 或 `organizer`。
*   **响应体示例**:
    ```json
    {
        "presentation_id": 1,
        "presentation_title": "我的第一次演讲",
        "total_feedbacks": 5,
        "feedback_counts": {
            "too_fast": 2,
            "boring": 1,
            "bad_question": 2
        }
    }
    ```

## 题目讨论区 (Discussion)

### 1. 添加评论
*   **URL**: `/discussion/questions/<int:question_id>/comments`
*   **方法**: `POST`
*   **描述**: 用户在题目停用后添加评论或回复。
*   **权限**: 需要有效的 JWT 访问令牌。
*   **请求体示例 (新评论)**:
    ```json
    {
        "comment_text": "我觉得这个题目很有趣！"
    }
    ```
*   **请求体示例 (回复评论)**:
    ```json
    {
        "comment_text": "同意，我也觉得很有趣。",
        "parent_comment_id": 1 // 回复 ID 为 1 的评论
    }
    ```
*   **响应体示例 (成功)**:
    ```json
    {
        "msg": "Comment added successfully",
        "comment_id": 1
    }
    ```
*   **响应体示例 (题目未停用)**:
    ```json
    {
        "msg": "Discussion is only available after question is deactivated"
    }
    ```

### 2. 获取评论
*   **URL**: `/discussion/questions/<int:question_id>/comments`
*   **方法**: `GET`
*   **描述**: 获取指定题目的所有评论（包括回复）。
*   **权限**: 需要有效的 JWT 访问令牌。
*   **响应体示例**:
    ```json
    [
        {
            "id": 1,
            "user_id": 2,
            "username": "listener_one",
            "comment_text": "我觉得这个题目很有趣！",
            "timestamp": "2025-07-19T16:45:00.123456",
            "replies": [
                {
                    "id": 2,
                    "user_id": 3,
                    "username": "listener_two",
                    "comment_text": "同意，我也觉得很有趣。",
                    "timestamp": "2025-07-19T16:46:00.789012",
                    "replies": []
                }
            ]
        }
    ]
    ```
*   **响应体示例 (题目未停用)**:
    ```json
    {
        "msg": "Discussion is only available after question is deactivated"
    }
    ```

## 文件管理 (Files)

### 1. 上传文件
*   **URL**: `/files/upload`
*   **方法**: `POST`
*   **描述**: 演讲者上传文件到 R2 对象存储。
*   **权限**: 需要有效的 JWT 访问令牌，且用户角色为 `speaker`。
*   **请求体**: `multipart/form-data`
    *   `file`: 要上传的文件。
    *   `presentation_id` (可选): 关联的演讲 ID。
*   **请求体示例 (使用 curl)**:
    ```bash
    curl -X POST \
      http://localhost:5000/api/files/upload \
      -H "Authorization: Bearer <YOUR_SPEAKER_JWT_TOKEN>" \
      -F "file=@/path/to/your/file.pdf" \
      -F "presentation_id=1" # Optional, if linking to a presentation
    ```
*   **响应体示例 (成功)**:
    ```json
    {
        "msg": "File uploaded successfully",
        "file_id": 1,
        "filename": "your_file.pdf",
        "s3_key": "unique_s3_key.pdf"
    }
    ```
*   **响应体示例 (失败 - 无文件)**:
    ```json
    {
        "msg": "No file part in the request"
    }
    ```
*   **响应体示例 (失败 - 未选择文件)**:
    ```json
    {
        "msg": "No selected file"
    }
    ```
*   **响应体示例 (失败 - S3/R2 未配置)**:
    ```json
    {
        "msg": "S3/R2 storage not configured"
    }
    ```
*   **响应体示例 (失败 - 演讲未找到)**:
    ```json
    {
        "msg": "Presentation not found"
    }
    ```
*   **响应体示例 (失败 - 未授权关联演讲)**:
    ```json
    {
        "msg": "You do not own this presentation"
    }
    ```
*   **响应体示例 (失败 - 上传失败)**:
    ```json
    {
        "msg": "Failed to upload file: <error_details>"
    }
    ```

### 2. 下载文件
*   **URL**: `/files/download/<int:file_id>`
*   **方法**: `GET`
*   **描述**: 组织者、观众或文件上传者下载文件。
*   **权限**: 需要有效的 JWT 访问令牌，且用户角色为 `organizer` 或 `listener`，或者用户是该文件的上传者。
*   **响应**: 文件内容作为附件下载。
*   **响应体示例 (失败 - 文件未找到)**:
    ```json
    {
        "msg": "File not found"
    }
    ```
*   **响应体示例 (失败 - 未授权)**:
    ```json
    {
        "msg": "Unauthorized to download this file"
    }
    ```
*   **响应体示例 (失败 - S3/R2 未配置)**:
    ```json
    {
        "msg": "S3/R2 storage not configured"
    }
    ```
*   **响应体示例 (失败 - 存储中未找到文件)**:
    ```json
    {
        "msg": "File not found in storage"
    }
    ```
*   **响应体示例 (失败 - 下载失败)**:
    ```json
    {
        "msg": "Failed to download file: <error_details>"
    }
    ```

### 3. 按演讲获取文件列表
*   **URL**: `/files/files_by_presentation/<int:presentation_id>`
*   **方法**: `GET`
*   **描述**: 获取指定演讲关联的所有文件元数据。
*   **权限**: 需要有效的 JWT 访问令牌，且用户是该演讲的 `speaker`、`organizer` 或 `listener`。
*   **响应体示例 (成功)**:
    ```json
    [
        {
            "id": 1,
            "filename": "presentation_slides.pdf",
            "upload_date": "2025-07-19T17:00:00.000000",
            "user_id": 1,
            "file_type": "application/pdf",
            "size": 102400
        },
        {
            "id": 2,
            "filename": "demo_code.zip",
            "upload_date": "2025-07-19T17:05:00.000000",
            "user_id": 1,
            "file_type": "application/zip",
            "size": 51200
        }
    ]
    ```
*   **响应体示例 (失败 - 演讲未找到)**:
    ```json
    {
        "msg": "Presentation not found"
    }
    ```
*   **响应体示例 (失败 - 未授权)**:
    ```json
    {
        "msg": "Unauthorized to view files for this presentation"
    }
    ```

## WebSocket 事件

### 1. 连接到演讲房间
*   **事件**: `join_presentation`
*   **描述**: 客户端连接到特定演讲的 WebSocket 房间，以接收实时更新。
*   **发送数据**:
    ```json
    {
        "presentation_id": 1 // 要加入的演讲 ID
    }
    ```
*   **接收事件**:
    *   `status`: 连接成功或失败的状态消息。
        ```json
        {"msg": "Joined presentation room 1"}
        ```
    *   `error`: 错误消息。
        ```json
        {"msg": "Unauthorized to join this presentation room"}
        ```
*   **权限**: 需要有效的 JWT 访问令牌。用户必须是该演讲的 `speaker`、`listener` 或 `organizer`。

### 2. 离开演讲房间
*   **事件**: `leave_presentation`
*   **描述**: 客户端离开特定演讲的 WebSocket 房间。
*   **发送数据**:
    ```json
    {
        "presentation_id": 1 // 要离开的演讲 ID
    }
    ```
*   **接收事件**:
    *   `status`: 离开成功或失败的状态消息。
        ```json
        {"msg": "Left presentation room 1"}
        ```
*   **权限**: 需要有效的 JWT 访问令牌。

### 3. 新题目推送
*   **事件**: `new_question`
*   **描述**: 当演讲者生成新题目时，后端会向所有连接到该演讲房间的客户端推送此事件。
*   **接收数据**:
    ```json
    {
        "id": 1,
        "question_text": "Flask 是一个什么类型的框架？",
        "question_type": "multiple_choice",
        "options": ["微框架", "全栈框架", "前端框架", "数据库框架"],
        "is_active": true
    }
    ```

### 4. 题目统计更新
*   **事件**: `question_stats_update`
*   **描述**: 当听众提交答案时，后端会向所有连接到该演讲房间的客户端推送此事件，更新该题目的实时统计。
*   **接收数据**:
    ```json
    {
        "question_id": 1,
        "question_text": "Flask 是一个什么类型的框架？",
        "total_answers": 5,
        "correct_answers": 3,
        "correct_rate": "60.00%",
        "option_distribution": {
            "微框架": 3,
            "全栈框架": 1,
            "前端框架": 1
        }
    }
