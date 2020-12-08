from PySide2 import QtCore, QtWidgets, QtGui, QtXml
from PySide2.QtUiTools import QUiLoader

import sys

from elvui_updater.downloader import Downloader
from elvui_updater.extractor import Extractor
from elvui_updater.resources import resources

loader = QUiLoader()


class UpdaterWindowWrapper(QtWidgets.QWidget):
    def __init__(self):
        super(UpdaterWindowWrapper, self).__init__()

        self._downloader = Downloader()

        self.ui = loader.load(":/ui/gui/gui.ui", None)
        self._connect_signals()

    def _connect_signals(self):
        self.ui.download_button.clicked.connect(self.download)
        self.ui.open_dialog.clicked.connect(self._select_wow_path)

    def _select_wow_path(self):
        dir_path = QtWidgets.QFileDialog.getExistingDirectory(
            self,
            "Wow dir",
            r"C:\Program Files (x86)\World of Warcraft\_retail_\Interface\AddOns",
        )
        if dir_path:
            self.ui.wow_path.setText(dir_path)

    def download(self):
        request = self._downloader.download()
        extractor = Extractor(request)
        extractor.extract(self.ui.wow_path.text())
        QtWidgets.QMessageBox.information(self, "ElvUI Updater", "Success!")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    updater_window = UpdaterWindowWrapper()
    updater_window.ui.show()
    sys.exit(app.exec_())
