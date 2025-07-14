package com.example.back.repository;

import com.example.back.entity.Presentation;
import com.example.back.entity.Quiz;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface QuizRepository extends JpaRepository<Quiz, Long> {
    List<Quiz> findByPresentation(Presentation presentation);
}
