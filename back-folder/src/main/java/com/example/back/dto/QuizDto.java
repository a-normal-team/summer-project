package com.example.back.dto;

import com.example.back.entity.Quiz;

import java.time.LocalDateTime;
import java.util.Map;

public class QuizDto {
    private Long id;
    private Long presentationId;
    private String question;
    private Map<String, String> options;
    private String correctAnswer; // Only for speaker/organizer or after quiz closed
    private String explanation;
    private String status;
    private LocalDateTime createdAt;

    public QuizDto() {
    }

    public QuizDto(Quiz quiz) {
        this.id = quiz.getId();
        this.presentationId = quiz.getPresentation().getId();
        this.question = quiz.getQuestion();
        this.options = quiz.getOptions();
        this.correctAnswer = quiz.getCorrectAnswer();
        this.explanation = quiz.getExplanation();
        this.status = quiz.getStatus().name();
        this.createdAt = quiz.getCreatedAt();
    }

    // Getters and Setters
    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public Long getPresentationId() {
        return presentationId;
    }

    public void setPresentationId(Long presentationId) {
        this.presentationId = presentationId;
    }

    public String getQuestion() {
        return question;
    }

    public void setQuestion(String question) {
        this.question = question;
    }

    public Map<String, String> getOptions() {
        return options;
    }

    public void setOptions(Map<String, String> options) {
        this.options = options;
    }

    public String getCorrectAnswer() {
        return correctAnswer;
    }

    public void setCorrectAnswer(String correctAnswer) {
        this.correctAnswer = correctAnswer;
    }

    public String getExplanation() {
        return explanation;
    }

    public void setExplanation(String explanation) {
        this.explanation = explanation;
    }

    public String getStatus() {
        return status;
    }

    public void setStatus(String status) {
        this.status = status;
    }

    public LocalDateTime getCreatedAt() {
        return createdAt;
    }

    public void setCreatedAt(LocalDateTime createdAt) {
        this.createdAt = createdAt;
    }
}
