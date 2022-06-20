import os

from PIL import Image, ImageQt
from PySide6.QtCore import SIGNAL, QSize, Qt
from PySide6.QtGui import QImage, QPixmap, QIcon
from PySide6.QtWidgets import QListWidget, QListWidgetItem


class DragDropListWidget(QListWidget):
    def __init__(self, type, parent=None):
        super(DragDropListWidget, self).__init__(parent)
        self.setAcceptDrops(True)
        self.setIconSize(QSize(72, 72))

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction)
            event.accept()
            l = []
            for url in event.mimeData().urls():
                l.append(str(url.toLocalFile()))
            self.emit(SIGNAL("dropped"), l)
        else:
            event.ignore()


    def pictureDropped(self, l):
        for url in l:
            if os.path.exists(url):
                picture = Image.open(url)
                picture.thumbnail((72, 72), Image.ANTIALIAS)
                icon = QIcon(QPixmap.fromImage(ImageQt.ImageQt(picture)))
                item = QListWidgetItem(os.path.basename(
                    url)[:20] + "...", self.pictureListWidget)
                item.setStatusTip(url)
                item.setIcon(icon)
