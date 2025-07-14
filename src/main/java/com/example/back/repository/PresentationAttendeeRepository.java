package com.example.back.repository;

import com.example.back.entity.Presentation;
import com.example.back.entity.PresentationAttendee;
import com.example.back.entity.PresentationAttendeeId;
import com.example.back.entity.User;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public interface PresentationAttendeeRepository extends JpaRepository<PresentationAttendee, PresentationAttendeeId> {
    List<PresentationAttendee> findByPresentation(Presentation presentation);
    List<PresentationAttendee> findByAttendee(User attendee);
    Optional<PresentationAttendee> findByPresentationAndAttendee(Presentation presentation, User attendee);
}
