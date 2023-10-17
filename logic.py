import os

from pytube import YouTube
from pytube.exceptions import VideoUnavailable


# Environment variables
SAVE_DIR = os.path.expanduser("~\\Downloads\\")


# Check correct input
def is_video_available(video: YouTube) -> bool:
    """
        Проверяет доступность видео на YouTube.
        Args:
            video: Объект видео.
        Returns:
            bool: Результат проверки доступности видео.
    """
    try:
        video.check_availability()
        return True
    except VideoUnavailable:
        print("Видео недоступно или не существует")
        return False
    except Exception as e:
        print(f"Произошла ошибка при проверке видео: {repr(e)}")
        return False


# Get the resolution list
def get_resolution_list(video: YouTube) -> []:
    """
            Возвращает доступные разрешения видео на YouTube.
            Args:
                video: Объект видео.
            Returns:
                []:  Список разрешений видео
        """
    video_resolutions = []
    for stream in video.streams.order_by('resolution'):
        video_resolutions.append(stream.resolution)
    return list(dict.fromkeys(video_resolutions))


# Download logic
def download_video(video_url: str,
                   audio_track: bool = False,
                   resolution: str = '720p'):
    try:
        video = YouTube(video_url)
        if is_video_available(video):
            stream = video.streams.filter(res=resolution,
                                          only_audio=audio_track,
                                          mime_type="video/mp4").first()
            stream.download(SAVE_DIR)
    except Exception as e:
        print(f"Произошла ошибка при скачивании видео: {repr(e)}")

