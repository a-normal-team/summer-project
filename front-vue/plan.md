# 任务列表

### 任务一用户角色：
- 实现组织者、演讲者、听众三种角色的用户注册、登录和权限管理功能
- 在系统中清晰地建立和管理“演讲者-课程（演讲）-听众”的关联关系

### 任务二输出与用户交互 (Web App)： 通过网页应用实现核心互动功能。

- 听众端： 能够接收并回答题目，提交后立即看到正确与否的反馈，并在演讲结束后查看个人统计报告（如正确率）。
- 演讲者端： 能够实时查看各题目的作答统计（如回答人数、正确率、选项分布等）。
- 组织者端： 能够管理和查看其组织的所有演讲活动。可以查看每场演讲的整体互动数据（参与人数、平均正确率等），以及每个听众在不同活动中的表现。
- 端到端演示： 系统需支持一个完整的演示流程，例如：使用两个不同的输入文件，生成5个选择题，包含1个组织者、1个演讲者和3个听众，完整展示从内容上传到最终报告的全过程。
- 即时反馈： 听众除了答题外，还可以发送“讲得太快”、“讲得太慢”、“内容乏味”、“题目质量差”等预设的即时反馈。这些反馈将汇总并展示在演讲者和组织者的报告中。
- 题目讨论区： 每个题目在回答截止后，自动生成一个即时讨论区，所有参与者可以就该题目和选项发表评论和交流。

### 任务三核心问题
- 生成选择题这个字任务中，需要调用大语言模型api根据演讲者上传的pdf或者文本内容和prompt生成题目


### 核心流程串讲 (演示场景)

1.  **准备阶段:**
    *   **组织者**登录，创建一场名为 "Spring Boot入门" 的演讲，并指派**演讲者A**。
    *   **演讲者A**登录，看到该演讲，进入管理页面，上传了他的 `SpringBoot.pptx`。
    *   **后端**收到文件，解析出每页的文字，存入 数据库 **以备演讲时使用**。
    *   **听众B, C, D**注册并加入该演讲。

2.  **演讲中:**
    *   **演讲者A**开始演讲
    *   10分钟后，**演讲者A**点击了“**生成随堂测验**”按钮。
    *   **后端**调用api生成问题
    *   AI在几秒内生成了一个新的选择题并返回。
    *   **后端**将题目存入数据库，并立刻通过WebSocket推送给**听众B, C, D**。
    *   **听众B, C, D**的手机/电脑上立刻弹出 **QuizModal**，显示题目和10秒倒计时。他们各自作答并提交。
    *   **演讲者A**的 界面针对这个新生成的题目进行实时更新，显示3人作答，2人正确，1人错误。
    *   **听众C**觉得有点快，点击了 "讲得太快" 按钮。**演讲者A**的 **FeedbackTicker** 上显示一条新反馈。

3.  **演讲后:**
    *   演讲结束，**演讲者A**点击 "结束演讲"。
    *   **听众B**进入 **PostPresentationReport** 页面，看到自己答对了4/5，正确率80%，排名第1。他可以回顾所有题目，并对第3题有疑问，点击进入讨论区发表了评论。
    *   **演讲者A**查看演讲报告，看到了每个题目的详细统计和收到的所有反馈。他看到了**听众B**的评论并进行了回复。
    *   **组织者**在他的 Dashboard 上看到 "Spring Boot入门" 演讲有3人参加，整体正确率为75%，是一次成功的分享。

### 前端设计计划

#### 1. 页面结构与设计

##### 1.1 认证相关页面

*   **登录页面 (`/login`)**
    *   **设计**: 简洁的登录表单，包含用户名、密码输入框和登录按钮。
    *   **交互**:
        *   用户输入凭据后点击登录。
        *   成功登录后，根据用户角色跳转到对应的仪表盘页面。
        *   登录失败（如凭据无效）显示错误消息。
    *   **API**: `POST /auth/login`

*   **注册页面 (`/register`)**
    *   **设计**: 注册表单，包含用户名、密码、确认密码输入框和注册按钮。可选的角色选择（默认为“listener”）。
    *   **交互**:
        *   用户填写信息后点击注册。
        *   成功注册后，跳转到登录页面。
        *   注册失败（如用户名已存在）显示错误消息。
    *   **API**: `POST /auth/register`

##### 1.2 通用页面

*   **仪表盘/主页 (`/dashboard`)**
    *   **设计**: 导航栏（包含用户角色、登出按钮），主内容区根据用户角色动态加载对应组件。
    *   **交互**:
        *   根据登录用户的角色（组织者、演讲者、听众）显示不同的内容。
        *   点击登出按钮清除JWT并跳转到登录页面。
    *   **API**: 无直接API调用，作为路由分发中心。

##### 1.3 组织者相关页面

*   **组织者仪表盘 (`/organizer/dashboard`)**
    *   **设计**:
        *   显示“我的演讲”列表，每项包含演讲标题、描述、演讲者、状态（进行中/已结束）。
        *   “创建新演讲”按钮。
        *   每个演讲项可点击进入详情管理页面。
    *   **交互**:
        *   点击“创建新演讲”按钮，弹出模态框或跳转到创建演讲页面。
        *   点击演讲列表项，跳转到该演讲的管理页面。
    *   **API**: `GET /presentations` (获取所有演讲，组织者可查看所有)

*   **创建/编辑演讲页面 (`/organizer/presentations/create` 或 `/organizer/presentations/:id/edit`)**
    *   **设计**: 表单包含演讲标题、描述输入框，以及指派演讲者的下拉选择框（可能需要获取用户列表）。
    *   **交互**:
        *   填写信息后提交，创建新演讲或更新现有演讲。
        *   成功后返回组织者仪表盘。
    *   **API**: `POST /presentations/create`, `PUT /presentations/<int:presentation_id>`

*   **演讲管理页面 (`/organizer/presentations/:id/manage`)**
    *   **设计**:
        *   显示演讲详情（标题、描述、演讲者）。
        *   “编辑演讲”和“删除演讲”按钮。
        *   “整体统计”区域：显示参与人数、平均正确率等 (`/quiz/presentations/<int:presentation_id>/overall_stats`)。
        *   “听众表现”列表：显示每个听众的作答情况 (`/quiz/presentations/<int:presentation_id>/overall_stats` 中的 `listener_performance`)。
        *   “文件列表”区域：显示该演讲关联的文件，可下载 (`/files/files_by_presentation/<int:presentation_id>`)。
        *   “反馈统计”区域：显示即时反馈汇总 (`/feedback/presentations/<int:presentation_id>/stats`)。
    *   **交互**:
        *   点击“编辑/删除”按钮执行相应操作。
        *   点击听众表现列表项，可查看该听众的个人报告（如果权限允许）。
        *   点击文件列表项，下载文件。
    *   **API**:
        *   `GET /presentations/<int:presentation_id>`
        *   `PUT /presentations/<int:presentation_id>`
        *   `DELETE /presentations/<int:presentation_id>`
        *   `GET /quiz/presentations/<int:presentation_id>/overall_stats`
        *   `GET /files/files_by_presentation/<int:presentation_id>`
        *   `GET /feedback/presentations/<int:presentation_id>/stats`
        *   `GET /files/download/<int:file_id>`

##### 1.4 演讲者相关页面

*   **演讲者仪表盘 (`/speaker/dashboard`)**
    *   **设计**: 显示“我的演讲”列表，每项包含演讲标题、描述、状态。
    *   **交互**:
        *   点击演讲列表项，跳转到该演讲的详情/管理页面。
    *   **API**: `GET /presentations` (过滤出当前演讲者创建的演讲)

*   **演讲详情/管理页面 (`/speaker/presentations/:id`)**
    *   **设计**:
        *   显示演讲详情（标题、描述）。
        *   “上传文件”区域：文件上传组件。
        *   “文件列表”区域：显示已上传文件，可删除或查看内容。
        *   “题目管理”区域：
            *   “生成随堂测验”按钮。
            *   当前活跃题目显示区（如果存在）。
            *   历史题目列表，每项可点击查看统计或进入讨论区。
        *   “实时统计”区域：显示当前活跃题目的实时作答统计 (`/quiz/presentations/<int:presentation_id>/active_question` 和 `question_stats_update` WebSocket事件)。
        *   “即时反馈”区域：显示收到的即时反馈汇总 (`/feedback/presentations/<int:presentation_id>/stats`)。
    *   **交互**:
        *   点击“上传文件”按钮上传文件。
        *   点击“生成随堂测验”按钮，触发后端生成题目。
        *   点击历史题目列表项，跳转到题目统计页面或讨论区。
        *   通过WebSocket实时更新题目统计和反馈。
    *   **API**:
        *   `GET /presentations/<int:presentation_id>`
        *   `POST /files/upload`
        *   `GET /files/files_by_presentation/<int:presentation_id>`
        *   `GET /files/<int:file_id>/content`
        *   `POST /quiz/presentations/<int:presentation_id>/questions` (生成题目)
        *   `GET /quiz/presentations/<int:presentation_id>/active_question`
        *   `POST /quiz/questions/<int:question_id>/deactivate`
        *   `GET /quiz/questions/<int:question_id>/stats`
        *   `GET /feedback/presentations/<int:presentation_id>/stats`
        *   **WebSocket**: `join_presentation`, `new_question`, `question_stats_update`

##### 1.5 听众相关页面

*   **听众仪表盘 (`/listener/dashboard`)**
    *   **设计**: 显示“可参与的演讲”列表，每项包含演讲标题、描述、演讲者。
    *   **交互**:
        *   点击演讲列表项，跳转到该演讲的参与页面。
    *   **API**: `GET /presentations` (获取所有演讲)

*   **演讲参与页面 (`/listener/presentations/:id`)**
    *   **设计**:
        *   显示演讲标题和描述。
        *   “当前题目”显示区：通过WebSocket接收并显示活跃题目（`new_question` WebSocket事件）。
        *   作答区域：根据题目类型（多选/单选）显示选项，并有提交按钮。
        *   “即时反馈”按钮组：包含“讲得太快”、“讲得太慢”、“内容乏味”、“题目质量差”等按钮。
        *   “查看个人报告”按钮（演讲结束后可见）。
    *   **交互**:
        *   接收到新题目时，弹出QuizModal或直接显示题目，并开始倒计时。
        *   用户选择答案后点击提交，立即显示正确与否的反馈。
        *   点击即时反馈按钮发送反馈。
        *   演讲结束后，点击“查看个人报告”按钮跳转。
    *   **API**:
        *   `GET /presentations/<int:presentation_id>`
        *   `GET /quiz/presentations/<int:presentation_id>/active_question`
        *   `POST /quiz/questions/<int:question_id>/answer`
        *   `POST /feedback/presentations/<int:presentation_id>/submit`
        *   **WebSocket**: `join_presentation`, `new_question`

*   **个人报告页面 (`/listener/presentations/:id/report`)**
    *   **设计**:
        *   显示个人作答概览（总题目数、已答题目数、正确数、正确率）。
        *   题目详情列表：每项显示题目、你的答案、正确答案、是否正确。
        *   每个题目项可点击进入讨论区（如果题目已停用）。
    *   **交互**:
        *   点击题目项，跳转到该题目的讨论区。
    *   **API**: `GET /quiz/presentations/<int:presentation_id>/report/<int:user_id>`

##### 1.6 通用组件

*   **QuizModal (模态框)**
    *   **设计**: 浮动在页面上方的模态框，显示题目、选项和倒计时。
    *   **交互**: 接收到`new_question`事件时弹出，倒计时结束或提交答案后关闭。

*   **题目讨论区页面 (`/discussion/questions/:id`)**
    *   **设计**:
        *   显示题目文本。
        *   评论列表，支持多级回复显示。
        *   评论输入框和提交按钮。
    *   **交互**:
        *   用户输入评论或回复后提交。
        *   实时加载和显示评论。
    *   **API**:
        *   `GET /discussion/questions/<int:question_id>/comments`
        *   `POST /discussion/questions/<int:question_id>/comments`

#### 2. 页面跳转逻辑

*   **未认证用户**:
    *   默认访问 `/login`。
    *   从 `/login` 可跳转到 `/register`。
    *   从 `/register` 成功后跳转回 `/login`。

*   **认证用户**:
    *   **登录成功后**:
        *   `listener` 角色跳转到 `/listener/dashboard`。
        *   `speaker` 角色跳转到 `/speaker/dashboard`。
        *   `organizer` 角色跳转到 `/organizer/dashboard`。
    *   **导航栏**: 所有登录用户都应有导航栏，包含“仪表盘”、“我的演讲/可参与的演讲”等链接，以及“登出”按钮。

*   **组织者**:
    *   `/organizer/dashboard` -> 点击“创建新演讲” -> 弹出模态框或跳转到 `/organizer/presentations/create`。
    *   `/organizer/dashboard` -> 点击演讲列表项 -> `/organizer/presentations/:id/manage`。
    *   `/organizer/presentations/:id/manage` -> 点击“编辑演讲” -> `/organizer/presentations/:id/edit`。

*   **演讲者**:
    *   `/speaker/dashboard` -> 点击演讲列表项 -> `/speaker/presentations/:id`。
    *   `/speaker/presentations/:id` -> 点击历史题目 -> `/discussion/questions/:id` (如果题目已停用) 或 `/speaker/quiz/questions/:id/stats` (查看统计)。

*   **听众**:
    *   `/listener/dashboard` -> 点击演讲列表项 -> `/listener/presentations/:id`。
    *   `/listener/presentations/:id` -> 演讲结束后点击“查看个人报告” -> `/listener/presentations/:id/report`。
    *   `/listener/presentations/:id/report` -> 点击题目详情 -> `/discussion/questions/:id` (如果题目已停用)。

*   **登出**:
    *   所有角色点击登出按钮 -> 清除JWT -> 跳转到 `/login`。

#### 3. 权限控制

*   **前端路由守卫**: 在Vue Router中使用导航守卫（`beforeEach`）检查用户是否已登录，并根据JWT中的角色信息判断是否有权访问特定路由。
*   **组件级权限**: 在组件内部根据用户角色动态显示或隐藏某些功能按钮或信息。
*   **API请求拦截器**: 在发送API请求时，自动附加JWT。后端会再次验证JWT和用户权限。

#### 4. 状态管理

*   使用Vuex或Pinia管理全局状态，如用户认证信息（JWT、用户ID、角色）、当前活跃演讲ID、WebSocket连接状态等。
*   演讲和题目数据可以在各自的页面组件中进行局部状态管理，或根据需要提升到全局状态。

#### 5. WebSocket集成

*   在 `main.ts` 或专门的WebSocket服务文件中初始化Socket.IO客户端。
*   在进入演讲参与/管理页面时（`listener/presentations/:id` 和 `speaker/presentations/:id`），发送 `join_presentation` 事件。
*   监听 `new_question` 和 `question_stats_update` 事件，并更新UI。
*   在离开页面时，发送 `leave_presentation` 事件。
