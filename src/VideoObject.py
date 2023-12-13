#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests

from pytube import YouTube
from collections import OrderedDict

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
        self.video_obj = YouTube(url_str)
        self.title = self.video_obj.title
        self.author = self.video_obj.author

        int_dur = self.video_obj.length
        str_dur = f"{int_dur // 3600}:{(int_dur % 3600) // 60:02d}:{int_dur % 60:02d}"
        self.duration = str_dur

        self.streams = self.video_obj.streams.order_by('resolution').desc()

        thumbnail_url = self.video_obj.thumbnail_url
        r = requests.get(thumbnail_url, allow_redirects=True, stream=False)

        self.thumbnail_img = r.content
        self.res_stream_dict = self.get_stream_dict()

    def get_stream_dict(self) -> dict:
        """
        Возвращает словарь из разрешений видео и 
        соответствующих им потоков для скачивания 
        """
        return OrderedDict((stream.resolution, stream) for stream in self.streams)
