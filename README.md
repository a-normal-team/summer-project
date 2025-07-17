# Ai-Pop-Quiz 后端服务

这是一个基于 Spring Boot 的后端服务，为 "Ai-Pop-Quiz" 应用程序提供核心功能。它负责用户认证、演示文稿管理、测验生成与管理，并可能集成人工智能能力以增强测验体验。

## 技术栈

*   **后端框架**: Spring Boot
*   **语言**: Java
*   **数据库**:
    *   关系型数据库 (通过 Spring Data JPA)
    *   MongoDB (通过 Spring Data MongoDB)
*   **构建工具**: Maven
*   **AI 集成**: 可能与 Google Gemini AI 模型集成 (通过 `GeminiService`)

## 项目结构

项目遵循典型的 Spring Boot 分层架构，主要包结构如下：

*   `com.example.back`: 项目根包。
    *   `BackApplication.java`: 应用程序的入口点。
    *   `config/`: 应用程序配置，例如安全配置、数据库配置等。
    *   `controller/`: RESTful API 控制器，处理 HTTP 请求。
        *   例如：`AuthController` (用户认证), `PresentationController` (演示文稿), `QuizController` (测验), `UserController` (用户数据)。
    *   `document/`: MongoDB 文档定义。
        *   `ContentChunk.java`: 演示文稿或测验内容的块。
        *   `Discussion.java`: 讨论或评论。
    *   `dto/`: 数据传输对象 (DTOs)，用于在不同层之间传递数据，通常用于请求和响应体。
        *   例如：`UserLoginRequest`, `QuizDto`, `AuthResponse`。
    *   `entity/`: 关系型数据库实体，通过 JPA 映射到数据库表。
        *   例如：`User`, `Presentation`, `Quiz`, `Feedback`。
    *   `exception/`: 自定义异常类。
    *   `mongorepository/`: MongoDB 数据访问接口 (Spring Data MongoDB Repository)。
        *   例如：`ContentChunkRepository`, `DiscussionRepository`。
    *   `repository/`: 关系型数据库数据访问接口 (Spring Data JPA Repository)。
        *   例如：`UserRepository`, `PresentationRepository`, `QuizRepository`。
    *   `service/`: 业务逻辑层，包含核心业务处理。
        *   例如：`AuthService` (认证), `PresentationService` (演示文稿), `QuizService` (测验), `GeminiService` (AI 集成)。
    *   `util/`: 通用工具类。
        *   例如：`HashMapConverter`。
*   `src/main/resources/`: 资源文件。
    *   `application.properties`: Spring Boot 应用程序的配置文件。
    *   `static/`: 静态资源文件 (如果后端提供静态文件服务)。
    *   `templates/`: 模板文件 (如果后端渲染页面)。
*   `src/test/`: 测试代码。
    *   `BackApplicationTests.java`: 应用程序的测试入口。
*   `pom.xml`: Maven 项目配置文件，定义依赖和构建过程。

## 如何运行项目

1.  **克隆仓库**:
    ```bash
    git clone https://github.com/a-normal-team/summer-project.git
    cd summer-project/back
    ```
2.  **配置数据库**:
    *   根据 `src/main/resources/application.properties` 配置您的关系型数据库和 MongoDB 连接信息。
3.  **构建项目**:
    ```bash
    ./mvnw clean install
    ```
4.  **运行项目**:
    ```bash
    ./mvnw spring-boot:run
    ```
    或者，您可以运行生成的 JAR 文件：
    ```bash
    java -jar target/back-0.0.1-SNAPSHOT.jar
    ```

项目将在默认端口 8080 上启动 (如果 `application.properties` 中未指定其他端口)。

## API 概览 (示例)

（此处可以添加更详细的 API 端点列表和用法，例如：）

*   **用户认证**:
    *   `POST /api/auth/register`: 用户注册
    *   `POST /api/auth/login`: 用户登录
*   **演示文稿**:
    *   `POST /api/presentations`: 创建演示文稿
    *   `GET /api/presentations/{id}`: 获取特定演示文稿
*   **测验**:
    *   `POST /api/quizzes/generate`: 生成测验
    *   `POST /api/quizzes/{id}/answer`: 提交测验答案

请参考源代码中的 `controller` 包以获取完整的 API 端点列表和请求/响应结构。
