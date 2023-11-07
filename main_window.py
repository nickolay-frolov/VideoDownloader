import sys

from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QWidget, QPushButton, QLineEdit, QComboBox, QCheckBox, QMainWindow, QLabel
from PySide6.QtCore import QFile, QIODevice
from pytube.exceptions import RegexMatchError, VideoUnavailable

from VideoObject import VideoObject
from environment import *


class MainWindow(QMainWindow):
    download_btn: QPushButton
    cancel_btn: QPushButton
    download_thumbnail_btn: QPushButton
    load_info_btn: QPushButton

    url_le: QLineEdit
    res_cb: QComboBox

    audio_chb: QCheckBox

    title_label: QLabel
    thumbnail_label: QLabel
    author_label: QLabel
    duration_label: QLabel
    def __init__(self):
        super().__init__()
        window = self.setup_ui()
        self.setCentralWidget(window)

        self.download_btn = window.findChild(QPushButton, "download_video_btn")
        self.cancel_btn = window.findChild(QPushButton, "cancel_btn")
        self.download_thumbnail_btn = window.findChild(QPushButton, "download_thumbnail_btn")
        self.load_info_btn = window.findChild(QPushButton, "load_info_btn")

        self.url_le = window.findChild(QLineEdit, "url_le")

        self.res_cb = window.findChild(QComboBox, "res_cb")
        self.audio_chb = window.findChild(QCheckBox, "audio_chb")

        self.title_label = window.findChild(QLabel, "title_label")
        self.thumbnail_label = window.findChild(QLabel, "thumbnail_label")
        self.author_label = window.findChild(QLabel, "author_label")
        self.duration_label = window.findChild(QLabel, "duration_label")

        self.download_btn.clicked.connect(self.on_download_click)
        self.cancel_btn.clicked.connect(self.on_close_click)
        self.load_info_btn.clicked.connect(self.on_load_click)
        self.url_le.setFocus()

    def setup_ui(self) -> QWidget:
        ui_file = QFile("mainWindow.ui")

        try:
            if not ui_file.open(QIODevice.ReadOnly):
                raise Exception(f"Ошибка открытия файла {ui_file}: "
                                f"{ui_file.errorString()}")

            loader = QUiLoader()
            window = loader.load(ui_file)

            if not window:
                raise Exception(loader.errorString())

        except Exception as e:
            print(f"Ошибка загрузки UI: {str(e)}")
            sys.exit(-1)

        finally:
            ui_file.close()

        return window

    def on_download_click(self):
        ...

    def on_close_click(self):
        sys.exit(0)

    def on_load_click(self):
        url_str = self.url_le.text()

        try:
            video = VideoObject(url_str)

            self.title_label.setText(video.title[:70] + '...' if len(video.title) > 70 else video.title)

            self.thumbnail_label.setPixmap(video.thumbnail_img)
            self.thumbnail_label.setScaledContents(True)

            self.author_label.setText(video.author)
            self.duration_label.setText(video.duration)

            self.res_cb.clear()
            self.res_cb.addItems(video.resolutions)
        except RegexMatchError:
            self.title_label.setText('Link is incorrect')
        except VideoUnavailable:
            self.title_label.setText('This video is not available')
