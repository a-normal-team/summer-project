package com.example.back.repository;

import com.example.back.entity.Presentation;
import com.example.back.entity.User;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface PresentationRepository extends JpaRepository<Presentation, Long> {
    List<Presentation> findBySpeaker(User speaker);
    List<Presentation> findByOrganizer(User organizer);
}
