package com.example.youtubeapi.service;

import com.example.youtubeapi.api.vm.YoutubeSoundtrackData;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

@Service
public class YoutubeService {

    public void getSoundtrackData(
            String baseUrl,
            String part,
            String q,
            int maxResultCount,
            String type,
            String key
    ) {
        RestTemplate restTemplate = new RestTemplate();

        String url = baseUrl + "?part=" + part + "&q=" + q + "&maxResults=" + maxResultCount + "&type=" + type + "&key=" + key;
        YoutubeSoundtrackData result = restTemplate.getForObject(url, YoutubeSoundtrackData.class);

        System.out.println(result);
    }
}
