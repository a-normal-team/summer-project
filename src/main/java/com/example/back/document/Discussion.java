package com.example.back.document;

import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;
import org.springframework.data.mongodb.core.mapping.Field;

import java.time.LocalDateTime;
import java.util.List;
import java.util.ArrayList;

@Document(collection = "discussions")
public class Discussion {
    @Id
    private String id; // MongoDB uses String for ObjectId

    @Field("quizId")
    private Long quizId; // 关联 MySQL quizzes.id

    @Field("comments")
    private List<Comment> comments = new ArrayList<>();

    // Getters and Setters
    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public Long getQuizId() {
        return quizId;
    }

    public void setQuizId(Long quizId) {
        this.quizId = quizId;
    }

    public List<Comment> getComments() {
        return comments;
    }

    public void setComments(List<Comment> comments) {
        this.comments = comments;
    }

    public static class Comment {
        @Field("commentId")
        private String commentId; // MongoDB uses String for ObjectId

        @Field("userId")
        private Long userId; // 关联 MySQL users.id

        @Field("username")
        private String username;

        @Field("text")
        private String text;

        @Field("timestamp")
        private LocalDateTime timestamp;

        @Field("replies")
        private List<Reply> replies = new ArrayList<>();

        // Getters and Setters
        public String getCommentId() {
            return commentId;
        }

        public void setCommentId(String commentId) {
            this.commentId = commentId;
        }

        public Long getUserId() {
            return userId;
        }

        public void setUserId(Long userId) {
            this.userId = userId;
        }

        public String getUsername() {
            return username;
        }

        public void setUsername(String username) {
            this.username = username;
        }

        public String getText() {
            return text;
        }

        public void setText(String text) {
            this.text = text;
        }

        public LocalDateTime getTimestamp() {
            return timestamp;
        }

        public void setTimestamp(LocalDateTime timestamp) {
            this.timestamp = timestamp;
        }

        public List<Reply> getReplies() {
            return replies;
        }

        public void setReplies(List<Reply> replies) {
            this.replies = replies;
        }
    }

    public static class Reply {
        @Field("commentId")
        private String commentId; // MongoDB uses String for ObjectId

        @Field("userId")
        private Long userId;

        @Field("username")
        private String username;

        @Field("text")
        private String text;

        @Field("timestamp")
        private LocalDateTime timestamp;

        // Getters and Setters
        public String getCommentId() {
            return commentId;
        }

        public void setCommentId(String commentId) {
            this.commentId = commentId;
        }

        public Long getUserId() {
            return userId;
        }

        public void setUserId(Long userId) {
            this.userId = userId;
        }

        public String getUsername() {
            return username;
        }

        public void setUsername(String username) {
            this.username = username;
        }

        public String getText() {
            return text;
        }

        public void setText(String text) {
            this.text = text;
        }

        public LocalDateTime getTimestamp() {
            return timestamp;
        }

        public void setTimestamp(LocalDateTime timestamp) {
            this.timestamp = timestamp;
        }
    }
}
