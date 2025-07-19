package com.example.back.mongorepository;

import com.example.back.document.Discussion;
import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
public interface DiscussionRepository extends MongoRepository<Discussion, String> {
    Optional<Discussion> findByQuizId(Long quizId);
}
