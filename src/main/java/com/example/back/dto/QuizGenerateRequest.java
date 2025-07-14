package com.example.back.dto;

public class QuizGenerateRequest {
    private Long presentationId;
    private String contextText; // Combined speech transcript and PPT text
    // Potentially other parameters for AI model tuning

    // Getters and Setters
    public Long getPresentationId() {
        return presentationId;
    }

    public void setPresentationId(Long presentationId) {
        this.presentationId = presentationId;
    }

    public String getContextText() {
        return contextText;
    }

    public void setContextText(String contextText) {
        this.contextText = contextText;
    }
}
