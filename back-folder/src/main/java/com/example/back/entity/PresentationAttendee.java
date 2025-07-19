package com.example.back.entity;

import jakarta.persistence.*;
import jakarta.persistence.*;
import java.io.Serializable;
import java.time.LocalDateTime;

@Entity
@Table(name = "presentation_attendees")
@IdClass(PresentationAttendeeId.class)
public class PresentationAttendee implements Serializable {
    @Id
    @ManyToOne
    @JoinColumn(name = "presentation_id", nullable = false)
    private Presentation presentation;

    @Id
    @ManyToOne
    @JoinColumn(name = "attendee_id", nullable = false)
    private User attendee;

    @Column(name = "registered_at", nullable = false)
    private LocalDateTime registeredAt;

    // Getters and Setters
    public Presentation getPresentation() {
        return presentation;
    }

    public void setPresentation(Presentation presentation) {
        this.presentation = presentation;
    }

    public User getAttendee() {
        return attendee;
    }

    public void setAttendee(User attendee) {
        this.attendee = attendee;
    }

    public LocalDateTime getRegisteredAt() {
        return registeredAt;
    }

    public void setRegisteredAt(LocalDateTime registeredAt) {
        this.registeredAt = registeredAt;
    }
}
