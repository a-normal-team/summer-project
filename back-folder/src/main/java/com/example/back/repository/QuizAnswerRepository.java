package com.example.back.repository;

import com.example.back.entity.Quiz;
import com.example.back.entity.QuizAnswer;
import com.example.back.entity.User;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public interface QuizAnswerRepository extends JpaRepository<QuizAnswer, Long> {
    List<QuizAnswer> findByQuiz(Quiz quiz);
    List<QuizAnswer> findByUser(User user);
    Optional<QuizAnswer> findByQuizAndUser(Quiz quiz, User user);
}
