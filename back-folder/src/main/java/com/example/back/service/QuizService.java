package com.example.back.service;

import com.example.back.dto.QuizAnswerRequest;
import com.example.back.dto.QuizDto;
import com.example.back.dto.QuizGenerateRequest;
import com.example.back.entity.Quiz;
import com.example.back.entity.User;

import java.util.List;
import java.util.Optional;

/**
 * 测验服务接口。
 * 定义了测验相关的业务操作，包括创建、查询、更新、删除、提交答案和更改状态。
 */
public interface QuizService {
    /**
     * 创建新的测验。
     * @param request 包含测验生成信息的请求对象。
     * @param currentUser 当前用户，作为测验的创建者。
     * @return 创建成功的测验实体。
     */
    Quiz createQuiz(QuizGenerateRequest request, User currentUser);

    /**
     * 根据ID获取测验的DTO。
     * @param id 测验ID。
     * @return 包含测验DTO的Optional，如果找不到则为空。
     */
    Optional<QuizDto> getQuizById(Long id);

    /**
     * 根据演示文稿ID获取测验列表。
     * @param presentationId 演示文稿ID。
     * @return 演示文稿下的测验DTO列表。
     */
    List<QuizDto> getQuizzesByPresentation(Long presentationId);

    /**
     * 更新测验信息。
     * @param id 测验ID。
     * @param quizDto 包含更新信息的测验DTO。
     * @param currentUser 当前用户，用于权限验证。
     * @return 更新后的测验DTO。
     */
    QuizDto updateQuiz(Long id, QuizDto quizDto, User currentUser); // For speaker/organizer to edit

    /**
     * 删除测验。
     * @param id 测验ID。
     * @param currentUser 当前用户，用于权限验证。
     */
    void deleteQuiz(Long id, User currentUser);

    /**
     * 提交测验答案。
     * @param request 包含测验答案的请求对象。
     * @param currentUser 当前用户，作为答案提交者。
     */
    void submitQuizAnswer(QuizAnswerRequest request, User currentUser);

    /**
     * 获取用户对指定测验的答案。
     * @param quizId 测验ID。
     * @param user 用户实体。
     * @return 包含用户答案的Optional，如果找不到则为空。
     */
    Optional<String> getUserQuizAnswer(Long quizId, User user);

    /**
     * 更改测验状态。
     * @param quizId 测验ID。
     * @param newStatus 新的测验状态。
     * @param currentUser 当前用户，用于权限验证。
     */
    void changeQuizStatus(Long quizId, Quiz.Status newStatus, User currentUser);
}
