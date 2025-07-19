package com.example.back.dto;

import java.util.Map;

public class QuizStatsDto {
    private Long quizId;
    private String question;
    private int totalAnswers;
    private double correctnessRate;
    private Map<String, Long> optionDistribution; // Option (A, B, C, D) -> Count

    public QuizStatsDto() {
    }

    public QuizStatsDto(Long quizId, String question, int totalAnswers, double correctnessRate, Map<String, Long> optionDistribution) {
        this.quizId = quizId;
        this.question = question;
        this.totalAnswers = totalAnswers;
        this.correctnessRate = correctnessRate;
        this.optionDistribution = optionDistribution;
    }

    // Getters and Setters
    public Long getQuizId() {
        return quizId;
    }

    public void setQuizId(Long quizId) {
        this.quizId = quizId;
    }

    public String getQuestion() {
        return question;
    }

    public void setQuestion(String question) {
        this.question = question;
    }

    public int getTotalAnswers() {
        return totalAnswers;
    }

    public void setTotalAnswers(int totalAnswers) {
        this.totalAnswers = totalAnswers;
    }

    public double getCorrectnessRate() {
        return correctnessRate;
    }

    public void setCorrectnessRate(double correctnessRate) {
        this.correctnessRate = correctnessRate;
    }

    public Map<String, Long> getOptionDistribution() {
        return optionDistribution;
    }

    public void setOptionDistribution(Map<String, Long> optionDistribution) {
        this.optionDistribution = optionDistribution;
    }
}
