package com.example.youtubeapi.advice;

import org.springframework.http.HttpStatus;

public class YoutubeAccessDeniedException extends RuntimeException{

    private HttpStatus httpStatus;

    public YoutubeAccessDeniedException(String message) {
        super(message);
    }
}
