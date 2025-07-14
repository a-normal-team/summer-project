package com.example.back.util;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;

import jakarta.persistence.AttributeConverter;
import jakarta.persistence.Converter;
import java.io.IOException;
import java.util.HashMap;
import java.util.Map;

@Converter
public class HashMapConverter implements AttributeConverter<Map<String, String>, String> {

    private final ObjectMapper objectMapper = new ObjectMapper();

    @Override
    public String convertToDatabaseColumn(Map<String, String> customerInfo) {
        try {
            return objectMapper.writeValueAsString(customerInfo);
        } catch (JsonProcessingException ex) {
            // Handle exception
            return null;
        }
    }

    @Override
    public Map<String, String> convertToEntityAttribute(String customerInfoJSON) {
        try {
            return objectMapper.readValue(customerInfoJSON, HashMap.class);
        } catch (IOException ex) {
            // Handle exception
            return null;
        }
    }
}
