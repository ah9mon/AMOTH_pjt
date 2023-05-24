package com.example.youtubeapi.api.vm;

import lombok.Getter;
import lombok.Setter;

import java.util.Map;

@Getter
@Setter
public class YoutubeApiResponse {
    private Map<String, Object>[] items;
}