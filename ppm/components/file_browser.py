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
from typing import List

from ppm.components import AbstractComponent
from ppm.components.constants import FOLDER_BROWSE_BUTTON, FOLDER_PATH
from ppm.components.file_viewer import FileViewerComponent
from ppm.components.main_window import MainWindowComponent
from PySide6 import QtCore, QtWidgets


class FileBrowserComponent(AbstractComponent):

    _path = os.path.expanduser("~")

    def __init__(self, main_window: MainWindowComponent, file_viewer: FileViewerComponent,
                 * args, **kwargs):
        """
        Initialise the FileBrowserComponent object, referencing the main window
        element.

        :param QtWidgets.QMainWindow main_window: The main window element of
            the UI.
        :param *args: variable length extra arguments to pass down
            to QtCore.QObject
        :param **kwargs: dictionary parameters to pass to QtCore.QObject
        """
        self.file_viewer = file_viewer
        super().__init__(main_window, *args, **kwargs)

        # Set the path label to the default initially
        self.set_path_label()

    def setup_signals(self):
        super().setup_signals()

        self.browse_button.clicked.connect(self.browse_files)

    def _find_widgets(self):
        labels: List[QtWidgets.QLineEdit] = \
            self.main_window.ui_component.findChildren(
                QtWidgets.QLineEdit)
        for l in labels:
            if l.objectName() == FOLDER_PATH:
                self.folder_path_label = l

        buttons: List[QtWidgets.QPushButton] = self.main_window.ui_component.findChildren(
            QtWidgets.QPushButton)
        for bt in buttons:
            if bt.objectName() == FOLDER_BROWSE_BUTTON:
                self.browse_button = bt

    def set_path_label(self):
        self.folder_path_label.setText(self._path)

    @QtCore.Slot()
    def browse_files(self):
        dlg = QtWidgets.QFileDialog()
        dlg.setFileMode(QtWidgets.QFileDialog.Directory)
        dlg.setViewMode(QtWidgets.QFileDialog.List)
        dlg.setDirectory(self._path)

        filenames = []
        if dlg.exec():
            filenames = dlg.selectedFiles()

        assert len(filenames) == 1

        self._path = filenames[0]
        self.set_path_label()

        self.file_viewer.populate_thumbnails(self._path)
