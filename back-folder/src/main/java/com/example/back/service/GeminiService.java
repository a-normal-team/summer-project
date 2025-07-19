package com.example.back.service;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.client.WebClient;
import reactor.core.publisher.Mono;

import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Service
public class GeminiService {

    @Value("${gemini.api.key}")
    private String geminiApiKey;

    private final WebClient webClient;
    private static final String GEMINI_API_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/models/";
    private static final String MODEL_NAME = "gemini-pro";

    public GeminiService(WebClient.Builder webClientBuilder) {
        this.webClient = webClientBuilder.baseUrl(GEMINI_API_BASE_URL).build();
    }

    public String processTextWithGemini(String text, String prompt) {
        String url = MODEL_NAME + ":generateContent?key=" + geminiApiKey;

        Map<String, Object> part1 = new HashMap<>();
        part1.put("text", prompt);

        Map<String, Object> part2 = new HashMap<>();
        part2.put("text", text);

        Map<String, Object> content = new HashMap<>();
        content.put("parts", List.of(part1, part2));

        Map<String, Object> requestBody = new HashMap<>();
        requestBody.put("contents", Collections.singletonList(content));

        Mono<Map> responseMono = webClient.post()
                .uri(url)
                .bodyValue(requestBody)
                .retrieve()
                .bodyToMono(Map.class);

        Map<String, Object> response = responseMono.block(); // Blocking call for simplicity, consider async for production

        if (response != null && response.containsKey("candidates")) {
            List<Map<String, Object>> candidates = (List<Map<String, Object>>) response.get("candidates");
            if (!candidates.isEmpty()) {
                Map<String, Object> firstCandidate = candidates.get(0);
                if (firstCandidate.containsKey("content")) {
                    Map<String, Object> contentMap = (Map<String, Object>) firstCandidate.get("content");
                    if (contentMap.containsKey("parts")) {
                        List<Map<String, Object>> parts = (List<Map<String, Object>>) contentMap.get("parts");
                        if (!parts.isEmpty()) {
                            Map<String, Object> firstPart = parts.get(0);
                            if (firstPart.containsKey("text")) {
                                return (String) firstPart.get("text");
                            }
                        }
                    }
                }
            }
        }
        return "Error: Could not process text with Gemini API or parse response.";
    }
}
