#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests

from pytube import YouTube
from collections import OrderedDict

from environment import *

class VideoObject:
    url_str: str
    is_available: bool
    title: str
    author: str
    duration: str
    streams: []
    thumbnail_img: bytes
    res_stream_dict: dict

    def __init__(self, url_str: str):
        youtube_obj = YouTube(url_str)
        
        self.title = youtube_obj.title
        self.author = youtube_obj.author

        int_dur = youtube_obj.length
        str_dur = f"{int_dur // 3600}:{(int_dur % 3600) // 60:02d}:{int_dur % 60:02d}"
        self.duration = str_dur

        self.video_streams = youtube_obj.streams.order_by('resolution').desc()
        self.audio_stream = youtube_obj.streams.filter(only_audio=True).order_by('abr').last()

        thumbnail_url = youtube_obj.thumbnail_url
        thumbnail_url = thumbnail_url[:thumbnail_url.rfind('/')] + '/maxresdefault.jpg'
        r = requests.get(thumbnail_url, allow_redirects=True, stream=False)

        self.thumbnail_img = r.content
        self.res_stream_dict = self.get_stream_dict()

    def get_stream_dict(self) -> dict:
        """
        Возвращает словарь из разрешений видео и 
        соответствующих им потоков для скачивания 
        """
        return OrderedDict((stream.resolution, stream) for stream in self.video_streams)
    
    def save_thumbnail(self):
        """
        Сохраняет превью видео
        в виде файла
        """
        thumbnail_file = SAVE_DIR + self.title + '_thumbnail' + IMAGE_FORMAT

        with open(thumbnail_file, 'wb') as f:
            f.write(self.thumbnail_img)

    def download_video(self, is_only_audio: bool, resolution: str):
        """
        Загружает выбранный поток
        видео или аудио в виде файла
        """
        try:
            if not is_only_audio:
                cur_stream = self.res_stream_dict.get(resolution)
                
                if cur_stream.is_progressive:
                    cur_stream.download(output_path=SAVE_DIR, 
                                        filename=self.title + VIDEO_FORMAT)
                else:
                    print('need audio')
            else:
                cur_stream = self.cur_video.audio_stream
                cur_stream.download(output_path=SAVE_DIR, 
                                    filename=self.title + AUDIO_FORMAT)
        except Exception as e:
             print(f"Ошибка скачивания видео: {str(e)}")