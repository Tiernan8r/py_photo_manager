#!/usr/bin/env python
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
import json
import os
import sys

# Required to guarantee that the 'ppm' module is accessible when
# this file is run directly.
if os.getcwd() not in sys.path:
    sys.path.append(os.getcwd())

import logging
import logging.config

from PySide6 import QtWidgets

from ppm.constants import LOG_FILENAME
from ppm.main_window import MainWindow


def main():
    setup_logging()
    logger = logging.getLogger(__name__)

    logger.debug("Initialising UI")

    initialise_ui(logger)


def setup_logging():
    base_path = os.path.dirname(os.path.abspath(__file__))
    logging_path = base_path + os.path.sep + LOG_FILENAME

    logging.config.fileConfig(logging_path, disable_existing_loggers=False)


def initialise_ui(logger: logging.Logger):

    app = QtWidgets.QApplication(sys.argv)

    logger.debug("Launching MainWindow")
    main_window = MainWindow()
    main_window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
