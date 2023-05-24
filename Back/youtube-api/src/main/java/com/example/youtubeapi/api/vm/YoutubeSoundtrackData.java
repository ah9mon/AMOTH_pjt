package com.example.youtubeapi.api.vm;

import lombok.Getter;
import lombok.RequiredArgsConstructor;
import lombok.Setter;

@Getter
@Setter
public class YoutubeSoundtrackData {
    private Object id;
    private Object title;
    private Object thumbnails;

    public YoutubeSoundtrackData(Object id, Object title, Object thumbnail) {
        this.id = id;
        this.title = title;
        this.thumbnails = thumbnail;
    }
}