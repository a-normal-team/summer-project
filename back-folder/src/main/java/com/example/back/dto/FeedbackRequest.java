package com.example.back.dto;

import com.example.back.entity.Feedback;

public class FeedbackRequest {
    private Long presentationId;
    private Feedback.FeedbackType feedbackType;
    private Long relatedQuizId; // Nullable

    // Getters and Setters
    public Long getPresentationId() {
        return presentationId;
    }

    public void setPresentationId(Long presentationId) {
        this.presentationId = presentationId;
    }

    public Feedback.FeedbackType getFeedbackType() {
        return feedbackType;
    }

    public void setFeedbackType(Feedback.FeedbackType feedbackType) {
        this.feedbackType = feedbackType;
    }

    public Long getRelatedQuizId() {
        return relatedQuizId;
    }

    public void setRelatedQuizId(Long relatedQuizId) {
        this.relatedQuizId = relatedQuizId;
    }
}
