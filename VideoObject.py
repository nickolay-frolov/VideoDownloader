import os
import requests

from PySide6.QtGui import QPixmap
from pytube import YouTube
from pytube.exceptions import VideoUnavailable


class VideoObject:
    url_str: str
    title: str
    author: str
    duration: str
    streams: []
    thumbnail_img: QPixmap
    resolutions: []

    def __init__(self, url_str):
        video_obj = YouTube(url_str)

        self.title = video_obj.title
        self.author = video_obj.author

        int_dur = video_obj.length
        str_dur = f"{int_dur // 3600}:{(int_dur % 3600) // 60:02d}:{ int_dur % 60:02d}"
        self.duration = str_dur

        self.streams = video_obj.streams.order_by('resolution').filter(progressive=True).desc()

        thumbnail_url = video_obj.thumbnail_url
        r = requests.get(thumbnail_url, allow_redirects=True, stream=False)

        self.thumbnail_img = QPixmap()
        self.thumbnail_img.loadFromData(r.content)
        self.resolutions = self.get_resolution_list()

    def get_resolution_list(self) -> []:
        """
            Возвращает доступные разрешения видео на YouTube.
            Returns:
                []:  Список разрешений видео
        """
        video_resolutions = []
        for stream in self.streams:
            video_resolutions.append(stream.resolution)
        return list(dict.fromkeys(video_resolutions))
