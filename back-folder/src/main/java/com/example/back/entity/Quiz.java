package com.example.back.entity;

import jakarta.persistence.*;
import java.time.LocalDateTime;
import java.util.Map;
import com.example.back.util.HashMapConverter;

@Entity
@Table(name = "quizzes")
public class Quiz {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne
    @JoinColumn(name = "presentation_id", nullable = false)
    private Presentation presentation;

    @Column(columnDefinition = "TEXT", nullable = false)
    private String question;

    @Convert(converter = HashMapConverter.class) // Custom converter for JSON
    @Column(columnDefinition = "JSON", nullable = false)
    private Map<String, String> options; // e.g., {"A": "Option 1", "B": "Option 2", ...}

    @Column(name = "correct_answer", nullable = false)
    private String correctAnswer; // e.g., "A"

    @Column(columnDefinition = "TEXT")
    private String explanation; // AI可生成

    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    private Status status;

    @Column(name = "created_at", nullable = false)
    private LocalDateTime createdAt;

    public enum Status {
        DRAFT, LIVE, CLOSED
    }

    // Getters and Setters
    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public Presentation getPresentation() {
        return presentation;
    }

    public void setPresentation(Presentation presentation) {
        this.presentation = presentation;
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

    public Status getStatus() {
        return status;
    }

    public void setStatus(Status status) {
        this.status = status;
    }

    public LocalDateTime getCreatedAt() {
        return createdAt;
    }

    public void setCreatedAt(LocalDateTime createdAt) {
        this.createdAt = createdAt;
    }
}
