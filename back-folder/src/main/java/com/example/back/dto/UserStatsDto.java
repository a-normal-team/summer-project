package com.example.back.dto;

public class UserStatsDto {
    private Long userId;
    private String username;
    private int totalQuizzesAnswered;
    private int correctAnswers;
    private double correctnessRate;
    private int rank; // Optional, if ranking is implemented

    public UserStatsDto() {
    }

    public UserStatsDto(Long userId, String username, int totalQuizzesAnswered, int correctAnswers, double correctnessRate, int rank) {
        this.userId = userId;
        this.username = username;
        this.totalQuizzesAnswered = totalQuizzesAnswered;
        this.correctAnswers = correctAnswers;
        this.correctnessRate = correctnessRate;
        this.rank = rank;
    }

    // Getters and Setters
    public Long getUserId() {
        return userId;
    }

    public void setUserId(Long userId) {
        this.userId = userId;
    }

    public String getUsername() {
        return username;
    }

    public void setUsername(String username) {
        this.username = username;
    }

    public int getTotalQuizzesAnswered() {
        return totalQuizzesAnswered;
    }

    public void setTotalQuizzesAnswered(int totalQuizzesAnswered) {
        this.totalQuizzesAnswered = totalQuizzesAnswered;
    }

    public int getCorrectAnswers() {
        return correctAnswers;
    }

    public void setCorrectAnswers(int correctAnswers) {
        this.correctAnswers = correctAnswers;
    }

    public double getCorrectnessRate() {
        return correctnessRate;
    }

    public void setCorrectnessRate(double correctnessRate) {
        this.correctnessRate = correctnessRate;
    }

    public int getRank() {
        return rank;
    }

    public void setRank(int rank) {
        this.rank = rank;
    }
}
