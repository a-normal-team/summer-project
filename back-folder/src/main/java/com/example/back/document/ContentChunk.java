package com.example.back.document;

import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;
import org.springframework.data.mongodb.core.mapping.Field;

import java.time.LocalDateTime;
import java.util.Map;

@Document(collection = "content_chunks")
public class ContentChunk {
    @Id
    private String id; // MongoDB uses String for ObjectId

    @Field("presentationId")
    private Long presentationId; // 关联 MySQL presentations.id

    @Field("sourceType")
    private String sourceType; // "PPTX", "PDF", "AUDIO_TRANSCRIPT"

    @Field("sourceName")
    private String sourceName;

    @Field("metadata")
    private Map<String, Object> metadata; // e.g., {"pageNumber": 5, "timestamp_seconds": 610}

    @Field("textContent")
    private String textContent;

    @Field("processedAt")
    private LocalDateTime processedAt;

    // Getters and Setters
    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public Long getPresentationId() {
        return presentationId;
    }

    public void setPresentationId(Long presentationId) {
        this.presentationId = presentationId;
    }

    public String getSourceType() {
        return sourceType;
    }

    public void setSourceType(String sourceType) {
        this.sourceType = sourceType;
    }

    public String getSourceName() {
        return sourceName;
    }

    public void setSourceName(String sourceName) {
        this.sourceName = sourceName;
    }

    public Map<String, Object> getMetadata() {
        return metadata;
    }

    public void setMetadata(Map<String, Object> metadata) {
        this.metadata = metadata;
    }

    public String getTextContent() {
        return textContent;
    }

    public void setTextContent(String textContent) {
        this.textContent = textContent;
    }

    public LocalDateTime getProcessedAt() {
        return processedAt;
    }

    public void setProcessedAt(LocalDateTime processedAt) {
        this.processedAt = processedAt;
    }
}
