package com.example.back.dto;

import java.util.List;

public class OverallStatsDto {
    private Long presentationId;
    private String presentationTitle;
    private int totalAttendees;
    private double averageCorrectnessRate;
    private List<QuizStatsDto> quizStats; // Detailed stats for each quiz in this presentation

    public OverallStatsDto() {
    }

    public OverallStatsDto(Long presentationId, String presentationTitle, int totalAttendees, double averageCorrectnessRate, List<QuizStatsDto> quizStats) {
        this.presentationId = presentationId;
        this.presentationTitle = presentationTitle;
        this.totalAttendees = totalAttendees;
        this.averageCorrectnessRate = averageCorrectnessRate;
        this.quizStats = quizStats;
    }

    // Getters and Setters
    public Long getPresentationId() {
        return presentationId;
    }

    public void setPresentationId(Long presentationId) {
        this.presentationId = presentationId;
    }

    public String getPresentationTitle() {
        return presentationTitle;
    }

    public void setPresentationTitle(String presentationTitle) {
        this.presentationTitle = presentationTitle;
    }

    public int getTotalAttendees() {
        return totalAttendees;
    }

    public void setTotalAttendees(int totalAttendees) {
        this.totalAttendees = totalAttendees;
    }

    public double getAverageCorrectnessRate() {
        return averageCorrectnessRate;
    }

    public void setAverageCorrectnessRate(double averageCorrectnessRate) {
        this.averageCorrectnessRate = averageCorrectnessRate;
    }

    public List<QuizStatsDto> getQuizStats() {
        return quizStats;
    }

    public void setQuizStats(List<QuizStatsDto> quizStats) {
        this.quizStats = quizStats;
    }
}
