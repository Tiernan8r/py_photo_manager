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
import sys

from PySide6 import QtCore, QtUiTools, QtWidgets

import ppm.components as comp
from ppm.constants import UI_FILENAME

logger = logging.getLogger(__name__)


class MainWindow(comp.MainWindowComponent):
    """
    A Class to handle the behaviour of the overall UI window
    """

    def __init__(self, *args, **kwargs):
        """
        Initialise the MainWindow object

        :param *args: variable length extra arguments to pass down
            to QMainWindow
        :param **kwargs: dictionary parameters to pass to QMainWindow
        """
        super().__init__(*args, **kwargs)

        logger.debug("Loading UI file")

        self.ui_component = self.load_ui()
        self.ui_component.setWindowTitle("Photo Manager")

        logger.debug("Initialising window components")

        self.file_viewer = comp.FileViewerComponent(self)
        self.file_browser = comp.FileBrowserComponent(self, self.file_viewer)

    def show(self):
        """
        Shows the loaded UI if hidden.
        """
        self.ui_component.show()

    def load_ui(self) -> QtWidgets.QWidget:
        """
        Reads the UI XML file and converts it into a QT widget,
        and returns the widget

        returns:
            QWidget: The Main Window element of our UI, with widget
            elements laid out as defined in the UI file.
        """
        # Load in the 'form.ui' file where the ui layout is defined
        path = os.path.join(os.path.dirname(__file__), UI_FILENAME)
        ui_file = QtCore.QFile(path)

        if not ui_file.open(QtCore.QIODevice.ReadOnly):
            logger.error(f"Cannot open {UI_FILENAME}: {ui_file.errorString()}")
            sys.exit(-1)

        # Load the file using the QT UI loader class and return the
        # ui widget representing the layout
        loader = QtUiTools.QUiLoader()
        ui_window = loader.load(ui_file)
        ui_file.close()
        if not ui_window:
            logger.error(loader.errorString())
            sys.exit(-1)

        logger.debug("Successfully loaded UI file")

        return ui_window
