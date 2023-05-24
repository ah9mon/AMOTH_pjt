package com.example.youtubeapi.api;

import com.example.youtubeapi.api.vm.YoutubeApiResponse;
import com.example.youtubeapi.api.vm.YoutubeSoundtrackData;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.client.RestTemplate;

import java.util.LinkedHashMap;
import java.util.Map;

@RestController
public class YoutubeApiController {
    @GetMapping("/api/youtube/soundtrack")
    public ResponseEntity<YoutubeSoundtrackData> getSoundtrack(
            @RequestParam(value = "movie_title", required = false) String movieTitle,
            @RequestParam(value = "music_title", required = false) String musicTitle
    ) {
        RestTemplate restTemplate = new RestTemplate();

        String key = "AIzaSyBQlfGK3IAomhdmUr0H4_4jq5x-ia7843Q";
        String baseUrl = "https://www.googleapis.com/youtube/v3/search";
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

        String url = baseUrl + "?part=" + part + "&q=" + q + "&maxResults=" + maxResultCount + "&type=" + type + "&key=" + key;
        YoutubeApiResponse result = restTemplate.getForObject(url, YoutubeApiResponse.class);

        Map<String, Object> item = result.getItems()[0];
        Map<String, Object> snippet = (LinkedHashMap<String, Object>) item.get("snippet");
        Map<String, Object> thumbnails = (LinkedHashMap<String, Object>) snippet.get("thumbnails");

        YoutubeSoundtrackData response = new YoutubeSoundtrackData(item.get("id"), snippet.get("title"), thumbnails.get("high"));

        return ResponseEntity.ok(response);
    }
}
