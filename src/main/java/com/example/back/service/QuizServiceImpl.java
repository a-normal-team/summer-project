package com.example.back.service;

import com.example.back.dto.QuizAnswerRequest;
import com.example.back.dto.QuizDto;
import com.example.back.dto.QuizGenerateRequest;
import com.example.back.entity.Presentation;
import com.example.back.entity.Quiz;
import com.example.back.entity.QuizAnswer;
import com.example.back.entity.User;
import com.example.back.repository.PresentationRepository;
import com.example.back.repository.QuizAnswerRepository;
import com.example.back.repository.QuizRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.util.List;
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

    // @Autowired
    // private AiService aiService; // Will be created later for AI quiz generation

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

        // Call AI service to generate quiz based on contextText
        // For now, create a dummy quiz
        Quiz quiz = new Quiz();
        quiz.setPresentation(presentation);
        quiz.setQuestion("Generated Question: " + request.getContextText().substring(0, Math.min(request.getContextText().length(), 50)) + "...");
        quiz.setOptions(null); // AI will generate options
        quiz.setCorrectAnswer(null); // AI will provide correct answer
        quiz.setExplanation(null); // AI will provide explanation
        quiz.setStatus(Quiz.Status.DRAFT); // Initial status
        quiz.setCreatedAt(LocalDateTime.now());
        return quizRepository.save(quiz);
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
        quizAnswer.setCorrect(request.getSelectedAnswer().equals(quiz.getCorrectAnswer()));
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
