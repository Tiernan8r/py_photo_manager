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
from ppm.components.constants import IMAGE_THUMBNAIL_VIEW
from ppm.components.main_window import MainWindowComponent
from PySide6 import QtWidgets, QtCore, QtGui


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

    def _supported_image_formats(self) -> List[str]:
        return [img.toStdString() for img in
                QtGui.QImageReader.supportedImageFormats()]

    def populate_thumbnails(self, dir: str):
        print("Finding images in directory:", dir)
        img_exts = self._supported_image_formats()

        self.grid_layout = QtWidgets.QGridLayout(self.image_thumbnails)
        self.grid_layout.setVerticalSpacing(30)

        row_in_grid_layout = 0
        # first_img_file_path = ""

        for file in os.scandir(dir):
            # TODO: Show subdirs
            if not file.is_file():
                continue

            full_path = file.path
            # Get the file extension, then drop the "." at the start
            ext = os.path.splitext(file.name)[-1][1:]
            print(f"Found file '{file.name}' with extension '{ext}'")
            if not ext.lower() in img_exts:
                print("File isn't an image file, skipping")
                continue

            img_label = QtWidgets.QLabel()
            img_label.setAlignment(QtCore.Qt.AlignCenter)

            text_label = QtWidgets.QLabel()
            text_label.setAlignment(QtCore.Qt.AlignCenter)

            pixmap = QtGui.QPixmap(full_path)
            pixmap = pixmap.scaled(
                QtCore.QSize(100, 100),
                QtCore.Qt.KeepAspectRatio,
                QtCore.Qt.SmoothTransformation)
            img_label.setPixmap(pixmap)
            text_label.setText(file.name)

            img_label.mousePressEvent = \
                lambda e, \
                index=row_in_grid_layout, \
                file_path=full_path: \
                self.on_thumbnail_click(e, index, file_path)

            text_label.mousePressEvent = img_label.mousePressEvent
            thumbnail = QtWidgets.QBoxLayout(
                QtWidgets.QBoxLayout.TopToBottom)
            thumbnail.addWidget(img_label)
            thumbnail.addWidget(text_label)

            self.grid_layout.addLayout(
                thumbnail, row_in_grid_layout, 0, QtCore.Qt.AlignCenter)

            # if row_in_grid_layout == 0:
            #     first_img_file_path = full_path
            row_in_grid_layout += 1

        # Automatically select the first file in the list during init
        # self.on_thumbnail_click(None, 0, first_img_file_path)

    def on_thumbnail_click(self, event, index, img_file_path):
        # Deselect all thumbnails in the image selector
        for text_label_index in range(len(self.grid_layout.children())):
            text_label = self.grid_layout.itemAtPosition(text_label_index, 0)\
                .itemAt(1).widget()
            text_label.setStyleSheet("background-color:none;")

        # Select the single clicked thumbnail
        text_label_of_thumbnail = self.grid_layout.itemAtPosition(index, 0)\
            .itemAt(1).widget()
        text_label_of_thumbnail.setStyleSheet("background-color:blue;")

        # Update the display's image
        # self.display_image.update_display_image(img_file_path)
