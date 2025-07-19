package com.example.back.service;

import com.example.back.document.ContentChunk;
import com.example.back.dto.QuizAnswerRequest;
import com.example.back.dto.QuizDto;
import com.example.back.dto.QuizGenerateRequest;
import com.example.back.entity.Presentation;
import com.example.back.entity.Quiz;
import com.example.back.entity.QuizAnswer;
import com.example.back.entity.User;
import com.example.back.mongorepository.ContentChunkRepository;
import com.example.back.repository.PresentationRepository;
import com.example.back.repository.QuizAnswerRepository;
import com.example.back.repository.QuizRepository;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.stream.Collectors;

@Service
public class QuizServiceImpl implements QuizService {

    @Autowired
    private QuizRepository quizRepository;

    @Autowired
    private PresentationRepository presentationRepository;

    @Autowired
    private QuizAnswerRepository quizAnswerRepository;

    @Autowired
    private GeminiService geminiService; // 注入 GeminiService

    @Autowired
    private ContentChunkRepository contentChunkRepository; // 注入 ContentChunkRepository

    private final ObjectMapper objectMapper = new ObjectMapper(); // 用于 JSON 解析

    @Override
    @Transactional
    public Quiz createQuiz(QuizGenerateRequest request, User currentUser) {
        Presentation presentation = presentationRepository.findById(request.getPresentationId())
                .orElseThrow(() -> new RuntimeException("Presentation not found")); // Custom exception

        // Authorization check: Only speaker or organizer of the presentation can create quizzes
        if (!currentUser.getId().equals(presentation.getSpeaker().getId()) &&
            !currentUser.getId().equals(presentation.getOrganizer().getId()) &&
            currentUser.getRole() != User.Role.ADMIN) {
            throw new RuntimeException("Unauthorized to create quiz for this presentation"); // Custom exception
        }

        // 1. 获取演示文稿的所有内容块并拼接成完整文本
        List<ContentChunk> contentChunks = contentChunkRepository.findByPresentationId(request.getPresentationId());
        String combinedText = contentChunks.stream()
                .map(ContentChunk::getTextContent)
                .collect(Collectors.joining("\n\n")); // 使用双换行符分隔不同内容块

        if (combinedText.isEmpty()) {
            throw new RuntimeException("No content found for the presentation to generate quizzes.");
        }

        // 2. 定义一个合适的 prompt，指导 Gemini 模型生成测验问题
        String prompt = "根据以下演示文稿内容，生成5道多项选择题。每道题包含问题、四个选项（A, B, C, D）、正确答案和解释。请以 JSON 数组的格式返回，每个对象代表一个测验问题。JSON 格式如下：\n" +
                        "[\n" +
                        "  {\n" +
                        "    \"question\": \"问题?\",\n" +
                        "    \"options\": {\n" +
                        "      \"A\": \"选项A\",\n" +
                        "      \"B\": \"选项B\",\n" +
                        "      \"C\": \"选项C\",\n" +
                        "      \"D\": \"选项D\"\n" +
                        "    },\n" +
                        "    \"correctAnswer\": \"A\",\n" +
                        "    \"explanation\": \"解释\"\n" +
                        "  }\n" +
                        "]";

        // 3. 调用 GeminiService 生成测验问题
        String geminiResponse = geminiService.processTextWithGemini(combinedText, prompt);

        // 4. 解析 Gemini 返回的 JSON 字符串
        List<Quiz> generatedQuizzes;
        try {
            // 使用 ObjectMapper 将 JSON 字符串解析为 List<Map<String, Object>>
            List<Map<String, Object>> quizMaps = objectMapper.readValue(geminiResponse, List.class);

            generatedQuizzes = quizMaps.stream().map(quizMap -> {
                Quiz quiz = new Quiz();
                quiz.setPresentation(presentation);
                quiz.setQuestion((String) quizMap.get("question"));
                // options 是 Map<String, String> 类型
                quiz.setOptions((Map<String, String>) quizMap.get("options"));
                quiz.setCorrectAnswer((String) quizMap.get("correctAnswer"));
                quiz.setExplanation((String) quizMap.get("explanation"));
                quiz.setStatus(Quiz.Status.DRAFT); // 初始状态为草稿
                quiz.setCreatedAt(LocalDateTime.now());
                return quiz;
            }).collect(Collectors.toList());

        } catch (JsonProcessingException e) {
            throw new RuntimeException("Failed to parse Gemini API response: " + e.getMessage(), e);
        }

        // 5. 保存生成的 Quiz 实体到数据库
        quizRepository.saveAll(generatedQuizzes);

        // 返回第一个生成的测验，或者可以考虑返回一个包含所有生成测验的列表
        // 这里为了兼容 createQuiz 的返回类型，暂时返回第一个。如果需要返回多个，需要修改接口定义。
        return generatedQuizzes.isEmpty() ? null : generatedQuizzes.get(0);
    }

    @Override
    public Optional<QuizDto> getQuizById(Long id) {
        return quizRepository.findById(id)
                .map(quiz -> {
                    // Logic to hide correct answer based on user role/quiz status
                    // For simplicity, always return full DTO for now, security will be handled by Spring Security
                    return new QuizDto(quiz);
                });
    }

    @Override
    public List<QuizDto> getQuizzesByPresentation(Long presentationId) {
        Presentation presentation = presentationRepository.findById(presentationId)
                .orElseThrow(() -> new RuntimeException("Presentation not found")); // Custom exception

        return quizRepository.findByPresentation(presentation).stream()
                .map(quiz -> {
                    // Logic to hide correct answer based on user role/quiz status
                    return new QuizDto(quiz);
                })
                .collect(Collectors.toList());
    }

    @Override
    @Transactional
    public QuizDto updateQuiz(Long id, QuizDto quizDto, User currentUser) {
        Quiz quiz = quizRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Quiz not found")); // Custom exception

        // Authorization check: Only speaker, organizer, or admin can update
        if (!currentUser.getId().equals(quiz.getPresentation().getSpeaker().getId()) &&
            !currentUser.getId().equals(quiz.getPresentation().getOrganizer().getId()) &&
            currentUser.getRole() != User.Role.ADMIN) {
            throw new RuntimeException("Unauthorized to update this quiz"); // Custom exception
        }

        quiz.setQuestion(quizDto.getQuestion());
        quiz.setOptions(quizDto.getOptions());
        quiz.setCorrectAnswer(quizDto.getCorrectAnswer());
        quiz.setExplanation(quizDto.getExplanation());
        quiz.setStatus(Quiz.Status.valueOf(quizDto.getStatus())); // Update status if needed
        return new QuizDto(quizRepository.save(quiz));
    }

    @Override
    @Transactional
    public void deleteQuiz(Long id, User currentUser) {
        Quiz quiz = quizRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Quiz not found")); // Custom exception

        // Authorization check: Only speaker, organizer, or admin can delete
        if (!currentUser.getId().equals(quiz.getPresentation().getSpeaker().getId()) &&
            !currentUser.getId().equals(quiz.getPresentation().getOrganizer().getId()) &&
            currentUser.getRole() != User.Role.ADMIN) {
            throw new RuntimeException("Unauthorized to delete this quiz"); // Custom exception
        }

        // Delete associated answers and discussions
        quizAnswerRepository.findByQuiz(quiz).forEach(quizAnswerRepository::delete);
        // discussionRepository.findByQuizId(quiz.getId()).ifPresent(discussionRepository::delete); // Uncomment when discussionRepository is ready

        quizRepository.delete(quiz);
    }

    @Override
    @Transactional
    public void submitQuizAnswer(QuizAnswerRequest request, User currentUser) {
        Quiz quiz = quizRepository.findById(request.getQuizId())
                .orElseThrow(() -> new RuntimeException("Quiz not found")); // Custom exception

        if (quiz.getStatus() != Quiz.Status.LIVE) {
            throw new RuntimeException("Quiz is not currently live for answers"); // Custom exception
        }

        // Check if user has already answered this quiz
        Optional<QuizAnswer> existingAnswer = quizAnswerRepository.findByQuizAndUser(quiz, currentUser);
        if (existingAnswer.isPresent()) {
            throw new RuntimeException("User has already answered this quiz"); // Custom exception
        }

        QuizAnswer quizAnswer = new QuizAnswer();
        quizAnswer.setQuiz(quiz);
        quizAnswer.setUser(currentUser);
        quizAnswer.setSelectedAnswer(request.getSelectedAnswer());
        quizAnswer.setIsCorrect(request.getSelectedAnswer().equals(quiz.getCorrectAnswer()));
        quizAnswer.setAnsweredAt(LocalDateTime.now());
        quizAnswerRepository.save(quizAnswer);
    }

    @Override
    public Optional<String> getUserQuizAnswer(Long quizId, User user) {
        Quiz quiz = quizRepository.findById(quizId)
                .orElseThrow(() -> new RuntimeException("Quiz not found")); // Custom exception

        return quizAnswerRepository.findByQuizAndUser(quiz, user)
                .map(QuizAnswer::getSelectedAnswer);
    }

    @Override
    @Transactional
    public void changeQuizStatus(Long quizId, Quiz.Status newStatus, User currentUser) {
        Quiz quiz = quizRepository.findById(quizId)
                .orElseThrow(() -> new RuntimeException("Quiz not found")); // Custom exception

        // Authorization check: Only speaker, organizer, or admin can change status
        if (!currentUser.getId().equals(quiz.getPresentation().getSpeaker().getId()) &&
            !currentUser.getId().equals(quiz.getPresentation().getOrganizer().getId()) &&
            currentUser.getRole() != User.Role.ADMIN) {
            throw new RuntimeException("Unauthorized to change quiz status"); // Custom exception
        }

        quiz.setStatus(newStatus);
        quizRepository.save(quiz);
    }
}
