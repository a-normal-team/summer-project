package com.example.back.dto;

import com.example.back.entity.Presentation;
import com.example.back.entity.User;

import java.time.LocalDateTime;

public class PresentationDto {
    private Long id;
    private String title;
    private String description;
    private Long speakerId;
    private String speakerUsername;
    private Long organizerId;
    private String organizerUsername;
    private String status;
    private LocalDateTime createdAt;

    public PresentationDto() {
    }

    public PresentationDto(Presentation presentation) {
        this.id = presentation.getId();
        this.title = presentation.getTitle();
        this.description = presentation.getDescription();
        this.speakerId = presentation.getSpeaker().getId();
        this.speakerUsername = presentation.getSpeaker().getUsername();
        this.organizerId = presentation.getOrganizer().getId();
        this.organizerUsername = presentation.getOrganizer().getUsername();
        this.status = presentation.getStatus().name();
        this.createdAt = presentation.getCreatedAt();
    }

    // Getters and Setters
    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getTitle() {
        return title;
    }

    public void setTitle(String title) {
        this.title = title;
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    public Long getSpeakerId() {
        return speakerId;
    }

    public void setSpeakerId(Long speakerId) {
        this.speakerId = speakerId;
    }

    public String getSpeakerUsername() {
        return speakerUsername;
    }

    public void setSpeakerUsername(String speakerUsername) {
        this.speakerUsername = speakerUsername;
    }

    public Long getOrganizerId() {
        return organizerId;
    }

    public void setOrganizerId(Long organizerId) {
        this.organizerId = organizerId;
    }

    public String getOrganizerUsername() {
        return organizerUsername;
    }

    public void setOrganizerUsername(String organizerUsername) {
        this.organizerUsername = organizerUsername;
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
