package com.example.youtubeapi.api;

import com.example.youtubeapi.advice.YoutubeAccessDeniedException;
import com.example.youtubeapi.api.response.YoutubeApiResponse;
import com.example.youtubeapi.api.response.YoutubeSoundtrackResponse;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.client.HttpClientErrorException;
import org.springframework.web.client.RestTemplate;

import java.util.LinkedHashMap;
import java.util.Map;

@Slf4j
@RestController
public class YoutubeApiController {
    @Value("${youtube.api.baseUrl}")
    private String baseUrl;
    @Value("${youtube.api.key}")
    private String youtubeKey;

    @GetMapping("/api/youtube/soundtrack")
    public ResponseEntity<YoutubeSoundtrackResponse> getSoundtrack(
            @RequestParam(value = "movie_title", required = false) String movieTitle,
            @RequestParam(value = "music_title", required = false) String musicTitle
    ) {
        RestTemplate restTemplate = new RestTemplate();
        String url = generateUrlString(movieTitle, musicTitle);
        YoutubeApiResponse result;
        try {
            result = restTemplate.getForObject(url, YoutubeApiResponse.class);
        } catch (HttpClientErrorException e) {
            log.error(e.getMessage());
            throw new YoutubeAccessDeniedException("The request cannot be completed");
        }

        Map<String, Object> item = result.getItems()[0];
        Map<String, Object> snippet = (LinkedHashMap<String, Object>) item.get("snippet");
        Map<String, Object> thumbnails = (LinkedHashMap<String, Object>) snippet.get("thumbnails");

        YoutubeSoundtrackResponse soundtrackData = new YoutubeSoundtrackResponse(item.get("id"), snippet.get("title"), thumbnails.get("high"));
        return ResponseEntity.ok(soundtrackData);
    }

    private String generateUrlString(
            String movieTitle,
            String musicTitle
    ) {
        String part = "snippet";
        int maxResultCount = 1;
        String q;
        String type;
        if (movieTitle != null) {
            q = musicTitle + " of " + movieTitle + " music";
            type = "video";
        } else {
            q = musicTitle + " soundtrack";
            type = "playlist";
        }

        return baseUrl + "?part=" + part + "&q=" + q + "&maxResults=" + maxResultCount + "&type=" + type + "&key=" + youtubeKey;
    }
}
