#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import re
import datetime
import traceback

from collections import OrderedDict
from pytube import YouTube
from moviepy.editor import * 

from environment import *

class VideoObject:
    url_str: str
    is_available: bool
    title: str
    __title_file: str
    author: str
    duration: str
    streams: []
    thumbnail_img: bytes
    res_stream_dict: dict

    def __init__(self, url_str: str):
        youtube_obj = YouTube(url_str)
        
        self.title = youtube_obj.title
        self.__title_file = re.sub(r'[^a-zA-Z0-9\s\-_]', '', self.title) # validate file name
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
        thumbnail_file = THUMB_DIR + self.__title_file + '_thumbnail' + IMAGE_FORMAT

        with open(thumbnail_file, 'wb') as f:
            f.write(self.thumbnail_img)

    def download_video(self, is_only_audio: bool, resolution: str):
        """
        Загружает выбранный поток
        видео или аудио в виде файла
        """
        video_stream = self.res_stream_dict.get(resolution)

        try:
            if not is_only_audio:
                if video_stream.is_progressive:
                    
                    video_stream.download(output_path=VIDEO_DIR, 
                                        filename=self.__title_file + VIDEO_FORMAT)
                else:
                    """
                    если поток не содержит аудио,
                    докачиваем отдельно и 
                    объединяем с видео 
                    """
                    audio_stream = self.audio_stream
                    
                    video_path = VIDEO_DIR + '\\' + self.__title_file + '_videopart' + VIDEO_FORMAT
                    audio_path = AUDIO_DIR + '\\' + self.__title_file + '_audiopart' + AUDIO_FORMAT

                    video_stream.download(output_path=VIDEO_DIR, 
                                        filename=self.__title_file + '_videopart' + VIDEO_FORMAT)
                    audio_stream.download(output_path=AUDIO_DIR, 
                                    filename=self.__title_file + '_audiopart' + AUDIO_FORMAT)
                    
                    video_file = VideoFileClip(video_path)
                    audio_file = AudioFileClip(audio_path)
                    
                    final_clip = video_file.set_audio(audio_file)
                    final_clip.write_videofile(VIDEO_DIR + '\\' + self.__title_file + VIDEO_FORMAT)

                    os.remove(video_path)
                    os.remove(audio_path)
            else:
                audio_stream = self.audio_stream
                audio_stream.download(output_path=AUDIO_DIR, 
                                    filename=self.__title_file + AUDIO_FORMAT)
        except Exception as e:
             print(f"Ошибка скачивания видео: {str(e)}")
             traceback.print_exc()