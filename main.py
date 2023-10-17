import sys
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QComboBox, QCheckBox
from PySide6.QtCore import QFile, QIODevice


def setup_ui() -> QWidget:
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


def on_download_click():
    ...


def on_close_click():
    sys.exit(0)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = setup_ui()
    window.show()

    download_btn = window.findChild(QPushButton, "download_btn")
    cancel_btn = window.findChild(QPushButton, "cancel_btn")

    url_left = window.findChild(QLineEdit, "url_le")
    res_cb = window.findChild(QComboBox, "res_cb")
    audio_cbh = window.findChild(QCheckBox, "audio")

    download_btn.clicked.connect(on_download_click)
    cancel_btn.clicked.connect(on_close_click)

    sys.exit(app.exec())



