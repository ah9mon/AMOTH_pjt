package com.example.youtubeapi.advice;

import lombok.Builder;
import lombok.Data;

@Builder
@Data
public class ErrorResponse {
    private String message;
    private int status;
}
