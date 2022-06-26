# py_photo_manager
# Copyright (C) 2022 Tiernan8r
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
import os

from ppm.workers.constants import THUMBNAIL_PIXEL_HEIGHT, THUMBNAIL_PIXEL_WIDTH
from PySide6 import QtCore, QtGui, QtWidgets


class _ThumbnailSignal(QtCore.QObject):
    result = QtCore.Signal(tuple)


class ThumbnailGeneratorWorker(QtCore.QRunnable):

    def __init__(self, file_path: str):
        super().__init__()
        self._path = file_path

        self.output = _ThumbnailSignal()

    @QtCore.Slot()
    def run(self):
        pixmap = self._gen_pixmap()

        self.output.result.emit((pixmap))

    @property
    def file_name(self) -> str:
        return os.path.basename(self._path)

    def _gen_pixmap(self) -> QtGui.QPixmap:
        pixmap = QtGui.QPixmap(self._path)

        pixmap_size = QtCore.QSize(
            THUMBNAIL_PIXEL_WIDTH, THUMBNAIL_PIXEL_HEIGHT)

        pixmap = pixmap.scaled(
            pixmap_size,
            QtCore.Qt.KeepAspectRatio,
            QtCore.Qt.SmoothTransformation)

        return pixmap

    def _gen_thumbnail(self) -> QtWidgets.QBoxLayout:
        img_label = QtWidgets.QLabel()
        img_label.setAlignment(QtCore.Qt.AlignCenter)

        text_label = QtWidgets.QLabel()
        text_label.setAlignment(QtCore.Qt.AlignCenter)

        pixmap = self._gen_pixmap()
        img_label.setPixmap(pixmap)
        text_label.setText(self.file_name)

        img_label.mousePressEvent = mouse_click_event  # type: ignore
        text_label.mousePressEvent = mouse_click_event  # type: ignore

        thumbnail = QtWidgets.QBoxLayout(
            QtWidgets.QBoxLayout.TopToBottom)
        thumbnail.addWidget(img_label)
        thumbnail.addWidget(text_label)

        return thumbnail
