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
from PySide6.QtWidgets import QMainWindow, QWidget


class MainWindowComponent(QMainWindow):
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

    def show(self):
        """
        Shows the loaded UI if hidden.
        """
        raise NotImplementedError()

    def load_ui(self) -> QWidget:
        """
        Reads the UI XML file and converts it into a QT widget,
        and returns the widget

        returns:
            QWidget: The Main Window element of our UI, with widget
            elements laid out as defined in the UI file.
        """
        raise NotImplementedError()

    @property
    def ui_component(self) -> QMainWindow:
        raise NotImplementedError()
