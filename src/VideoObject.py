#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unicodedata
import requests
import re
import traceback

from collections import OrderedDict
from pytube import YouTube, StreamQuery, Stream
from moviepy.editor import * 

from environment import *

class VideoObject:
    youtube_obj: YouTube
    title: str
    __title_file: str
    author: str
    duration: str
    video_streams: StreamQuery
    thumbnail_img: bytes
    res_stream_dict: dict

    def __init__(self, url_str: str):
        self.youtube_obj = YouTube(url_str)
        
        self.title = self.youtube_obj.title
        
        # валидация имени файла
        self.__title_file = re.sub(r'[^a-zA-ZА-Яа-я0-9~@#$%^-_()\[\]{}\'`\s\-_\.]', '', self.title) 
        
        self.author = self.youtube_obj.author
        self.duration = self.get_duration()

        self.video_streams = self.youtube_obj.streams.filter(file_extension='mp4').order_by('resolution').desc()
        self.audio_stream = self.youtube_obj.streams.filter(only_audio=True).order_by('abr').last()

        self.thumbnail_img = self.get_thumbnail()
        self.res_stream_dict = self.get_stream_dict()

    def get_stream_dict(self) -> dict:
        """
        Возвращает словарь из разрешений видео и 
        соответствующих им потоков для скачивания 
        """
        # for stream in self.video_streams:
        #   print(stream)
        return OrderedDict((stream.resolution + self.get_filesize(stream),
                            stream) for stream in self.video_streams)
    
    def get_duration(self) -> str:
        int_dur = self.youtube_obj.length
        return f"{int_dur // 3600}:{(int_dur % 3600) // 60:02d}:{int_dur % 60:02d}"
    
    def get_thumbnail(self) -> bytes:
        thumbnail_url = self.youtube_obj.thumbnail_url
        
        # получение максимального качества из всех доступных
        thumbnail_url = thumbnail_url[:thumbnail_url.rfind('/')] + '/maxresdefault.jpg'
        thumbnail = requests.get(thumbnail_url, allow_redirects=True, stream=False)
        return thumbnail.content
    
    def get_filesize(self, stream: Stream) -> str:
        size_mb = stream.filesize / (1024 * 1024)
        if size_mb >= 1024:
            size_gb = size_mb / 1024
            remain_mb = size_mb % 1024
            return f" {int(size_gb)}GB {round(remain_mb, 2)}MB"
        else:
            return f" {round(size_mb, 2)}MB"

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