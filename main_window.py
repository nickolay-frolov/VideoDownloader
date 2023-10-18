import sys
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QWidget, QPushButton, QLineEdit, QComboBox, QCheckBox, QMainWindow
from PySide6.QtCore import QFile, QIODevice


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        window = self.setup_ui()
        self.setCentralWidget(window)

        self.download_btn = window.findChild(QPushButton, "download_btn")
        self.cancel_btn = window.findChild(QPushButton, "cancel_btn")

        self.url_le = window.findChild(QLineEdit, "url_le")
        self.res_cb = window.findChild(QComboBox, "res_cb")
        self.audio_cbh = window.findChild(QCheckBox, "audio")

        self.download_btn.clicked.connect(self.on_download_click)
        self.cancel_btn.clicked.connect(self.on_close_click)

    def setup_ui(self) -> QWidget:
        ui_file = QFile("mainWindow.ui")

        try:
            if not ui_file.open(QIODevice.ReadOnly):
                raise Exception(f"Cannot open {ui_file}: {ui_file.errorString()}")

            loader = QUiLoader()
            window = loader.load(ui_file)

            if not window:
                raise Exception(loader.errorString())

        except Exception as e:
            print(f"Error during UI setup: {str(e)}")
            sys.exit(-1)

        finally:
            ui_file.close()

        return window

    def on_download_click(self):
        text = self.url_le.text()
        print(text)

    def on_close_click(self):
        self.url_le.setText('')
        # sys.exit(0)