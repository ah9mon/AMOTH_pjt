package com.example.youtubeapi.api.response;

import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class YoutubeSoundtrackResponse {
    private Object id;
    private Object title;
    private Object thumbnails;

    public YoutubeSoundtrackResponse(Object id, Object title, Object thumbnail) {
        this.id = id;
        this.title = title;
        this.thumbnails = thumbnail;
    }
}