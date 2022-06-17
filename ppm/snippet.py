import os

from PySide6 import QtGui


def fileDropped(self, file):
    f = str(file[-1])

    if os.path.splitext(f)[1][1:] != 'tif':
      reply = QtGui.QMessageBox.question(self, 'Message', 'All files must be TIF images. Would you like me to convert a copy of your file to the TIF format?', QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)

      if reply == QtGui.QMessageBox.Yes:
        if not os.path.exists('./djvu_backup/'):  os.mkdir('./djvu_backup/')



        if f not in self.getChildren(self.ui.pageList):   # It's a custom method. It does what it looks like it does.
          icon = QtGui.QIcon(f)
          pixmap = icon.pixmap(72, 72)
          icon = QtGui.QIcon(pixmap)
          item = QtGui.QListWidgetItem(f, self.ui.pageList)
          item.setIcon(icon)
          item.setStatusTip(f)

        return True
