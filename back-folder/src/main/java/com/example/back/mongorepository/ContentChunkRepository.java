package com.example.back.mongorepository;

import com.example.back.document.ContentChunk;
import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface ContentChunkRepository extends MongoRepository<ContentChunk, String> {
    List<ContentChunk> findByPresentationId(Long presentationId);
}
