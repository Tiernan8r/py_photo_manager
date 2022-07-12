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
import logging
import os
from typing import List

from ppm.components import AbstractComponent
from ppm.components.constants import (FOLDER_BROWSE_BUTTON, FOLDER_PATH,
                                      FOUND_WIDGET_LOG_MESSAGE)
from ppm.components.main_window import MainWindowComponent
from ppm.components.thumbnail_viewer import ThumbnailViewerComponent
from PySide6 import QtCore, QtWidgets

logger = logging.getLogger(__name__)


class FileBrowserComponent(AbstractComponent):

    _path = os.path.expanduser("~")

    def __init__(self, main_window: MainWindowComponent,
                 thumbnail_viewer: ThumbnailViewerComponent,
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
        self.thumbnail_viewer = thumbnail_viewer
        super().__init__(main_window, *args, **kwargs)

        # Set the path label to the default initially
        self.set_path_label()

    def setup_signals(self):
        super().setup_signals()

        logger.debug("Setting browse button click signals")
        self.browse_button.clicked.connect(self.browse_files)

    def _find_widgets(self):
        labels: List[QtWidgets.QLineEdit] = \
            self.main_window.ui_component.findChildren(
                QtWidgets.QLineEdit)
        for lab in labels:
            if lab.objectName() == FOLDER_PATH:
                self.folder_path_label = lab
                logger.debug(FOUND_WIDGET_LOG_MESSAGE.format(FOLDER_PATH))

        buttons: List[QtWidgets.QPushButton] = \
            self.main_window.ui_component.findChildren(QtWidgets.QPushButton)
        for bt in buttons:
            if bt.objectName() == FOLDER_BROWSE_BUTTON:
                self.browse_button = bt
                logger.debug(FOUND_WIDGET_LOG_MESSAGE.format(
                    FOLDER_BROWSE_BUTTON))

    def set_path_label(self):
        logger.debug(
            f"Setting the folder_path_label value to be '{self._path}'")
        self.folder_path_label.setText(self._path)

    @QtCore.Slot()
    def browse_files(self):
        logger.debug(
            f"Spawning QFileDialog starting at the path '{self._path}'")

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

        logger.debug(f"File dialog opened to path '{self._path}'")

        self.thumbnail_viewer.populate_thumbnails(self._path)
