package com.example.back.entity;

import java.io.Serializable;
import java.util.Objects;

public class PresentationAttendeeId implements Serializable {
    private Long presentation; // Corresponds to presentation_id in PresentationAttendee
    private Long attendee;     // Corresponds to attendee_id in PresentationAttendee

    public PresentationAttendeeId() {
    }

    public PresentationAttendeeId(Long presentation, Long attendee) {
        this.presentation = presentation;
        this.attendee = attendee;
    }

    // Getters and Setters
    public Long getPresentation() {
        return presentation;
    }

    public void setPresentation(Long presentation) {
        this.presentation = presentation;
    }

    public Long getAttendee() {
        return attendee;
    }

    public void setAttendee(Long attendee) {
        this.attendee = attendee;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        PresentationAttendeeId that = (PresentationAttendeeId) o;
        return Objects.equals(presentation, that.presentation) &&
               Objects.equals(attendee, that.attendee);
    }

    @Override
    public int hashCode() {
        return Objects.hash(presentation, attendee);
    }
}
