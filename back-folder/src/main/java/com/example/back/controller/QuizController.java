package com.example.back.controller;

import com.example.back.dto.QuizDto;
import com.example.back.dto.QuizGenerateRequest;
import com.example.back.entity.Quiz;
import com.example.back.entity.User;
import com.example.back.service.QuizService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.stream.Collectors;

@RestController
@RequestMapping("/api/quizzes")
public class QuizController {

    @Autowired
    private QuizService quizService;

    // 假设有一个方法来获取当前认证的用户，这里简化处理
    // 实际应用中会通过 Spring Security 的 AuthenticationPrincipal 或其他方式获取
    private User getCurrentUser() {
        // 这是一个占位符方法，实际应用中需要根据认证机制获取当前用户
        // 例如，从 SecurityContextHolder 获取
        User user = new User();
        user.setId(1L); // 示例用户ID
        user.setUsername("testuser");
        user.setRole(User.Role.SPEAKER); // 示例角色
        return user;
    }

    @PostMapping("/generate")
    public ResponseEntity<QuizDto> generateQuiz(@RequestBody QuizGenerateRequest request) {
        // 在实际应用中，@AuthenticationPrincipal User currentUser 会自动注入当前用户
        User currentUser = getCurrentUser(); // 临时获取当前用户

        try {
            Quiz generatedQuiz = quizService.createQuiz(request, currentUser);
            // 返回生成的第一个测验的 DTO
            return new ResponseEntity<>(new QuizDto(generatedQuiz), HttpStatus.CREATED);
        } catch (RuntimeException e) {
            // 实际应用中应该返回更具体的错误信息和状态码
            return new ResponseEntity<>(HttpStatus.BAD_REQUEST);
        }
    }

    @GetMapping("/{id}")
    public ResponseEntity<QuizDto> getQuizById(@PathVariable Long id) {
        return quizService.getQuizById(id)
                .map(quizDto -> new ResponseEntity<>(quizDto, HttpStatus.OK))
                .orElse(new ResponseEntity<>(HttpStatus.NOT_FOUND));
    }

    @GetMapping("/presentation/{presentationId}")
    public ResponseEntity<List<QuizDto>> getQuizzesByPresentation(@PathVariable Long presentationId) {
        List<QuizDto> quizzes = quizService.getQuizzesByPresentation(presentationId);
        return new ResponseEntity<>(quizzes, HttpStatus.OK);
    }

    // 其他测验相关的API端点，例如更新、删除、提交答案等，可以根据需要添加
}
