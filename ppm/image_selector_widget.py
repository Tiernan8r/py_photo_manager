from os import listdir
from os.path import isfile, join

from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QBoxLayout, QGridLayout, QLabel, QWidget


# Widget for selecting an image in the directory to display
# Makes a vertical scrollable widget with selectable image thumbnails
class ImageFileSelector(QWidget):
    def __init__(self, parent=None, album_path='', display_image=None):
        QWidget.__init__(self, parent=parent)
        self.display_image = display_image
        self.grid_layout = QGridLayout(self)
        self.grid_layout.setVerticalSpacing(30)

        # Get all the image files in the directory
        files = [f for f in listdir(album_path) if isfile(join(album_path, f))]
        row_in_grid_layout = 0
        first_img_file_path = ''

        # Render a thumbnail in the widget for every image in the directory
        for file_name in files:
            if filename_has_image_extension(file_name) is False:
                continue
            img_label = QLabel()
            text_label = QLabel()
            img_label.setAlignment(Qt.AlignCenter)
            text_label.setAlignment(Qt.AlignCenter)

            file_path = album_path + file_name

            pixmap = QPixmap(file_path)
            pixmap = pixmap.scaled(
                QSize(100, 100),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation)
            img_label.setPixmap(pixmap)
            text_label.setText(file_name)
            img_label.mousePressEvent = \
                lambda e, \
                index=row_in_grid_layout, \
                file_path=file_path: \
                self.on_thumbnail_click(e, index, file_path)
            text_label.mousePressEvent = img_label.mousePressEvent
            thumbnail = QBoxLayout(QBoxLayout.TopToBottom)
            thumbnail.addWidget(img_label)
            thumbnail.addWidget(text_label)
            self.grid_layout.addLayout(
                thumbnail, row_in_grid_layout, 0, Qt.AlignCenter)

            if row_in_grid_layout == 0:
                first_img_file_path = file_path
            row_in_grid_layout += 1

        # Automatically select the first file in the list during init
        self.on_thumbnail_click(None, 0, first_img_file_path)

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
        self.display_image.update_display_image(img_file_path)


def filename_has_image_extension(file_name: str):
    # TODO: This...
    return True
