package com.example.back.repository;

import com.example.back.entity.Feedback;
import com.example.back.entity.Presentation;
import com.example.back.entity.User;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface FeedbackRepository extends JpaRepository<Feedback, Long> {
    List<Feedback> findByPresentation(Presentation presentation);
    List<Feedback> findByUser(User user);
}
