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
import typing

from ppm.components import AbstractComponent
from ppm.components.constants import IMAGE_THUMBNAIL_CONTENTS, IMAGE_THUMBNAIL_VIEW
from ppm.components.main_window import MainWindowComponent
from PySide6 import QtCore, QtGui, QtWidgets

logger = logging.getLogger(__name__)


class FileViewerComponent(AbstractComponent):

    def __init__(self, main_window: MainWindowComponent,
                 *args, **kwargs):
        """
        Initialise the FileViewerComponent object, referencing the main window
        element.

        :param QtWidgets.QMainWindow main_window: The main window element of
            the UI.
        :param *args: variable length extra arguments to pass down
            to QtCore.QObject
        :param **kwargs: dictionary parameters to pass to QtCore.QObject
        """
        super().__init__(main_window, *args, **kwargs)

    def _find_widgets(self):
        scroll_areas: List[QtWidgets.QScrollArea] = \
            self.main_window.ui_component.findChildren(
                QtWidgets.QScrollArea)
        for sa in scroll_areas:
            if sa.objectName() == IMAGE_THUMBNAIL_VIEW:
                self.image_thumbnails = sa
                logger.debug(
                    f"Found widget for the key '{IMAGE_THUMBNAIL_VIEW}'")

        widgets: List[QtWidgets.QWidget] = self.main_window.ui_component.findChildren(
            QtWidgets.QWidget)
        for wdgt in widgets:
            if wdgt.objectName() == IMAGE_THUMBNAIL_CONTENTS:
                self.image_thumbnail_contents = wdgt
                logger.debug(
                    f"Found widget for the key '{IMAGE_THUMBNAIL_CONTENTS}'")

    def _supported_image_formats(self) -> List[str]:
        return [img.toStdString() for img in
                QtGui.QImageReader.supportedImageFormats()]

    def get_image_files(self, dir: str) -> List[str]:
        # TODO: include subdirs...
        img_exts = self._supported_image_formats()

        files = []
        for file in os.scandir(dir):
            if not file.is_file():
                continue
            full_path = file.path
            # Get the file extension, then drop the "." at the start
            ext = os.path.splitext(file.name)[-1][1:]
            logger.debug(f"Found file '{file.name}' with extension '{ext}'")

            if not ext.lower() in img_exts:
                logger.debug("File isn't an image file, skipping")
                continue

            files.append(full_path)

        return sorted(files)

    def populate_thumbnails(self, dir: str):
        logger.debug(f"Populating image thumbnails in directory '{dir}'")

        self.grid_layout = QtWidgets.QGridLayout(self.image_thumbnail_contents)
        self.grid_layout.setVerticalSpacing(30)

        row_in_grid_layout = 0

        for file in self.get_image_files(dir):

            def custom_mouse_press(event,
                                   index=row_in_grid_layout,
                                   file_path=file):
                self.on_thumbnail_click(event, index, file_path)

            thumbnail = self._create_thumbnail(file, custom_mouse_press)

            self.grid_layout.addLayout(
                thumbnail, row_in_grid_layout, 0, QtCore.Qt.AlignCenter)

            row_in_grid_layout += 1

        logger.debug(f"DONE populating {row_in_grid_layout + 1} thumbnails")

    def _create_thumbnail(self, file_path: str, mouse_click_event: typing.Callable):
        file_name = os.path.basename(file_path)

        img_label = QtWidgets.QLabel()
        img_label.setAlignment(QtCore.Qt.AlignCenter)

        text_label = QtWidgets.QLabel()
        text_label.setAlignment(QtCore.Qt.AlignCenter)

        pixmap = QtGui.QPixmap(file_path)
        pixmap = pixmap.scaled(
            QtCore.QSize(100, 100),
            QtCore.Qt.KeepAspectRatio,
            QtCore.Qt.SmoothTransformation)
        img_label.setPixmap(pixmap)
        text_label.setText(file_name)

        img_label.mousePressEvent = mouse_click_event  # type: ignore
        text_label.mousePressEvent = mouse_click_event  # type: ignore

        thumbnail = QtWidgets.QBoxLayout(
            QtWidgets.QBoxLayout.TopToBottom)
        thumbnail.addWidget(img_label)
        thumbnail.addWidget(text_label)

        return thumbnail

    def on_thumbnail_click(self, event, index, img_file_path):
        logger.debug(f"Image '{img_file_path}' has been clicked")

        # Deselect all thumbnails in the image selector
        for text_label_index in range(len(self.grid_layout.children())):
            text_label = self.grid_layout.itemAtPosition(text_label_index, 0) \
                .itemAt(1).widget()
            text_label.setStyleSheet("background-color:none;")

        # Select the single clicked thumbnail
        text_label_of_thumbnail = self.grid_layout.itemAtPosition(index, 0)\
            .itemAt(1).widget()
        text_label_of_thumbnail.setStyleSheet("background-color:blue;")

        # Update the display's image
        # self.display_image.update_display_image(img_file_path)
