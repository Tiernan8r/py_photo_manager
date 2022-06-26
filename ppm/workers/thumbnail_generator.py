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
from PySide6 import QtCore, QtGui


class ThumbnailSignal(QtCore.QObject):
    result = QtCore.Signal(tuple)


class ThumbnailGeneratorWorker(QtCore.QRunnable):

    def __init__(self, file_path: str):
        super().__init__()
        self._file_path = file_path

        self.output = ThumbnailSignal()

    @QtCore.Slot()
    def run(self):
        pixmap = QtGui.QPixmap(self._file_path)
        pixmap = pixmap.scaled(
            QtCore.QSize(100, 100),
            QtCore.Qt.KeepAspectRatio,
            QtCore.Qt.SmoothTransformation)

        self.output.result.emit((pixmap))
