#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QWidget, QPushButton, QLineEdit, QComboBox, QCheckBox, QMainWindow, QLabel
from PySide6.QtCore import QFile, QIODevice
from pytube.exceptions import RegexMatchError, VideoUnavailable
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt

from videoObject import VideoObject
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

    cur_video: VideoObject

    def __init__(self):
        super().__init__()
        window = self.setup_ui()

        self.setCentralWidget(window)
        self.setWindowTitle('Video Downloader')
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        
        self.draggable = True
        self.offset = None
        
        self.download_btn = window.findChild(QPushButton, "download_video_btn")
        self.cancel_btn = window.findChild(QPushButton, "cancel_btn")
        self.download_thumbnail_btn = window.findChild(QPushButton, "download_thumbnail_btn")
        self.load_info_btn = window.findChild(QPushButton, "load_info_btn")
        self.cancel_min_btn = window.findChild(QPushButton, "cancel_min_btn")
        self.minimize_btn = window.findChild(QPushButton, "minimize_btn")

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
        self.download_thumbnail_btn.clicked.connect(self.on_thumbnail_save_click)
        self.cancel_min_btn.clicked.connect(self.on_close_click)
        self.minimize_btn.clicked.connect(self.on_minimize_click)

        self.url_le.setFocus()

        self.check_save_dir()


    #load user interface
    def setup_ui(self) -> QWidget:
        ui_file = QFile("src\mainWindow.ui")
        style_file = QFile("styles\mainWindow_styles.qss")

        try:
            if not ui_file.open(QIODevice.ReadOnly):
                raise Exception(f"Ошибка открытия UI файла {ui_file}: "
                                f"{ui_file.errorString()}")

            if not style_file.open(QIODevice.ReadOnly):
                raise Exception(f"Ошибка открытия QSS файла {style_file}: "
                                f"{style_file.errorString()}")

            loader = QUiLoader()
            window = loader.load(ui_file)

            self.setStyleSheet(style_file.readAll().data().decode("utf-8"))

            if not window:
                raise Exception(loader.errorString())

        except Exception as e:
            print(f"Ошибка загрузки UI: {str(e)}")
            sys.exit(-1)

        finally:
            ui_file.close()
            style_file.close()

        return window
    
    # move window
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and self.draggable:
            self.offset = event.pos()

    def mouseMoveEvent(self, event):
        if self.offset is not None and self.draggable:
            self.move(self.pos() + event.pos() - self.offset)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and self.draggable:
            self.offset = None

    # check exist save directories
    def check_save_dir(self):
       if not os.path.exists(SAVE_DIR):
           os.makedirs(SAVE_DIR)
       
       subdirectories = [VIDEO_DIR, AUDIO_DIR, THUMB_DIR]
       for subdirectory in subdirectories:
            if not os.path.exists(subdirectory):
               os.makedirs(subdirectory) 

    # load video info
    def on_load_click(self):
        url_str = self.url_le.text()

        try:
            self.cur_video = VideoObject(url_str)
            self.title_label.setText(self.cur_video.title[:70] + '...'
                                     if len(self.cur_video.title) > 70 
                                     else self.cur_video.title)

            thumbnail_map = QPixmap()
            thumbnail_map.loadFromData(self.cur_video.thumbnail_img)

            self.thumbnail_label.setPixmap(thumbnail_map)
            self.thumbnail_label.setScaledContents(True)

            self.author_label.setText(self.cur_video.author)
            self.duration_label.setText(self.cur_video.duration)

            self.res_cb.clear()
            self.res_cb.addItems(list(self.cur_video.res_stream_dict.keys()))
        except RegexMatchError:
            self.title_label.setText('Link is incorrect')
        except VideoUnavailable:
            self.title_label.setText('This video is not available')
    
    def on_thumbnail_save_click(self):
        self.cur_video.save_thumbnail()

    def on_download_click(self):
        is_only_audio = self.audio_chb.isChecked()
        resolution = self.res_cb.currentText()
        self.cur_video.download_video(is_only_audio, resolution)

    def on_minimize_click(self):
        self.showMinimized()

    def on_close_click(self):
        sys.exit(0)
