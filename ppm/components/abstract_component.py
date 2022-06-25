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

from ppm.components.main_window import MainWindowComponent
from PySide6 import QtCore

logger = logging.getLogger(__name__)


class AbstractComponent(QtCore.QObject):

    def __init__(self, main_window: MainWindowComponent, *args, **kwargs):
        """
        Setup the UI component, referencing the MainWindow UI element

        :param QtWidgets.QMainWindow main_window: The main window
            element of our UI.
        :param *args: variable length extra arguments to pass down
            to QtCore.QObject
        :param **kwargs: dictionary parameters to pass to QtCore.QObject
        """
        logger.debug("Initialising AbstractComponent")
        super().__init__(*args, **kwargs)
        self.main_window = main_window
        self.setup_signals()

    def setup_signals(self):
        """
        Setup any UI signals and events associated with interacting with
        this part of the UI.
        """
        logger.debug("Setting up AbstractComponent signals")
        logger.debug("Finding widgets...")
        self._find_widgets()

    def _find_widgets(self):
        """
        Searches the UI elements to get python object references to the ones
        that are relevant to the operation of this UI component.
        """
        pass
