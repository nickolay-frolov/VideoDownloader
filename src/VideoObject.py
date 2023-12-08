import requests

from pytube import YouTube


class VideoObject:
    url_str: str
    is_available: bool
    title: str
    author: str
    duration: str
    streams: []
    thumbnail_img: bytes
    resolutions: []

    def __init__(self, url_str: str):
        self.video_obj = YouTube(url_str)
        self.title = self.video_obj.title
        self.author = self.video_obj.author

        int_dur = self.video_obj.length
        str_dur = f"{int_dur // 3600}:{(int_dur % 3600) // 60:02d}:{int_dur % 60:02d}"
        self.duration = str_dur

        self.streams = self.video_obj.streams.order_by('resolution').filter(progressive=True).desc()

        thumbnail_url = self.video_obj.thumbnail_url
        r = requests.get(thumbnail_url, allow_redirects=True, stream=False)

        self.thumbnail_img = r.content
        # self.thumbnail_img.loadFromData(r.content)

        self.resolutions = self.get_resolution_list()

    def get_resolution_list(self) -> []:
        """
            Возвращает доступные разрешения видео на YouTube.
            Returns:
                []: Список разрешений видео
        """
        video_resolutions = []
        for stream in self.streams:
            video_resolutions.append(stream.resolution)
        return list(dict.fromkeys(video_resolutions))
